import argparse
from rich.console import Console
from rich import print
from rich.table import Table
from dotenv import load_dotenv, find_dotenv
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import sqlite3
import time
import shutil
import os
from jinja2 import Template
from markdownify import markdownify as md
import markdown
import re



load_dotenv(find_dotenv())


console = Console()


# *****************************************************************************************
# Define commandline flags and arguments
# *****************************************************************************************

parser = argparse.ArgumentParser(
    description="Generate a quiz from an epub"
)
parser.add_argument(
    "action",
    choices=[
        "init",
        "load",
        "transform",
        "list",
        "undo",
        "get"
    ],
    help="The action to perform ",
)


parser.add_argument("--db", help="The database file", required=False, default="promptlab.db")
parser.add_argument("--fn", help="Filename", required=False, default="test.epub")
parser.add_argument("--description", help="Description of the operations", required=False, default="")
parser.add_argument("--tag", help="Tag to filter on", required=False, default="*")
parser.add_argument("--script", help="Script to execute", required=False)
parser.add_argument("--blockid", help="Block ID to use", required=False)

args = parser.parse_args()

# *****************************************************************************************
# Utiltiy functions
# *****************************************************************************************
# If the db exists; if not, print error and exit.  Otherwise sqlite silently create a new file.
def check_db(fn):
    if not os.path.isfile(fn):
        console.log("Database file", fn, "does not exist.  Check the filename or run init to create a new database.")
        exit(1)

def load(fn):
    if not os.path.isfile(fn):
        raise Exception(f"File does not exist:{fn}" )
    # Load and return the file
    with open(fn, "r") as f:
        data = f.read()
    return data


# *****************************************************************************************
# Block operations
# *****************************************************************************************

# Write an operation to the database
def create_operation(c, operation, description=args.description):
    sql = load("sql/create_operation.sql")
    c.execute(sql, (operation, description))
    operation_id = c.lastrowid
    return operation_id

# Inserts into the blocks table and returns the block id
def create_block(c, operation_id, block, position, tag):
    sql = load("sql/create_block.sql")
    token_count = len(str(block).split(" "))
    c.execute(sql, (operation_id, position, block, token_count, tag))
    block_id = c.lastrowid
    return block_id

def execute(script,block):
    # Create a dictionary to use as the local variables
    loc = {}
    # Execute the code, using the block as the input
    loc['block'] = block
    exec(script, globals(), loc)
    # Return the result
    return loc['result']

def fetch_blocks(tag="*", latest=True):
    # Replace the * with a pct, which is what sqlite3 requires for wildcards
    tag = tag.replace("*", "%")
    if latest:
        sql = load("sql/fetch_latest_blocks.sql")
    else:
        sql = load("sql/fetch_blocks.sql")
    # Grab the data
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(sql, (tag,))
    results = c.fetchall()
    conn.close()
    return results

def fetch_blocks_by_id(id):
    # Replace the * with a pct, which is what sqlite3 requires for wildcards
    sql = load("sql/fetch_block_by_id.sql")
    # Grab the data
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(sql, (id,))
    results = c.fetchall()
    conn.close()
    return results

# *****************************************************************************************
# Action operations 
# *****************************************************************************************

# Initialize the database by reading in the schema and creating the database
def action_init():
    # Back up the existing database
    try:
        now = time.strftime("%Y%m%d-%H%M%S")
        # copy the db to a backup file
        backup_fn = args.db + "." + now + ".bak"
        console.log("Backing up database to", backup_fn)
        shutil.copyfile(args.db, backup_fn)
        os.remove(args.db)
    except:
        pass
    # Initialize the new database
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    sql = load("sql/schema.sql")
    c.executescript(sql)
    conn.commit()
    conn.close()

# Loads a file into the database
def action_load():
    console.log("Loading file", args.fn)
    # If the load fails then we want to rollback the entire transaction
    try:
        conn = sqlite3.connect(args.db)
        conn.isolation_level = None
        c = conn.cursor()
        c.execute("BEGIN")
        operation_id = create_operation(c, "load", "Loading file " + args.fn)
        # Load the file based on the filetype
        if args.fn.endswith(".epub"):
            book = epub.read_epub(args.fn)
            for idx,item in enumerate(book.get_items()):
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    html = item.get_content().decode("utf-8")
                    create_block(c, operation_id, html, idx, item.get_name())
            conn.commit()
        else:
            txt = load(args.fn)
            create_block(c, operation_id, txt, 0, args.fn)
            conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()

def action_undo():
    console.log("Undoing last operation")
    sql = load("sql/undo_operation.sql")
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys=ON");
    c.execute(sql)
    conn.commit()
    conn.close()

def action_transform(script):
    console.log("Transforming file", args.fn)
    script = load(script)
    blocks = fetch_blocks(args.tag)
    # Open a new connection
    conn = sqlite3.connect(args.db)
    conn.isolation_level = None
    c = conn.cursor()
    c.execute("BEGIN")
    operation_id = create_operation(c, "transform", "Transforming file " + args.fn)
    try:
        for b in blocks:
            console.log("Processing block", b['tag'])
            result = execute(script, b['block'])
            if type(result) is list:
                for idx,r in enumerate(result):
                    create_block(c, operation_id, r, idx, b['tag'])
            elif type(result) is str:
                create_block(c, operation_id, result, 0, b['tag'])
            else:
                # Raise an error
                raise Exception(f"Result is not a list or string: {type(result)}")
        conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()

def action_list():
    console.log("Listing blocks")
    blocks = fetch_blocks(args.tag)
    table = Table(title="Blocks", header_style="bold magenta")
    table.add_column("operation_id", justify="center")
    table.add_column("operation", justify="center")
    table.add_column("block_id", justify="center", style="cyan")
    table.add_column("tag", justify="left")
    table.add_column("token_count", justify="right")
    table.add_column("block", justify="left")
    for block in blocks:
        # Strip and \n and replace with " " for block
        b = str(block["block"]).replace("\n", " ")
        table.add_row(
            str(block["operation_id"]),
            block["operation"],
            str(block["id"]),
            block["tag"],
            '{:,}'.format(block["token_count"]),
            b[:20],
        )
    console.print(table)

def action_get():
    if args.blockid is not None:
        blocks = fetch_blocks_by_id(args.blockid)
    else:
        blocks = fetch_blocks(args.tag)
    # Pull out the block element into it's own list
    out = [b['block'] for b in blocks]
    console.print("\n".join(out))



# --------------------------------------------------------------------------------------------
# Begin actions
# --------------------------------------------------------------------------------------------

if args.action == 'init':
    action_init()
    console.log("Initialized database")
    exit(0)

if args.action == 'load':
    check_db(args.db)
    if args.fn is None:
        console.log("You must provide a --fn argument for the file to read")
        exit(1)
    action_load()

if args.action =='transform':
    check_db(args.db)
    if args.fn is None:
        console.log("You must provide a --fn argument for the file to read")
        exit(1)
    if args.script is None:
        console.log("You must provide a --script argument for the script to execute")
        exit(1)
    action_transform(args.script)

if args.action == 'list':
    check_db(args.db)
    action_list()
    exit(0)

if args.action == 'undo':
    check_db(args.db)
    action_undo()
    exit(0)

if args.action == 'get':
    check_db(args.db)
    action_get()
    exit(0)
    

    



