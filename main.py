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
import sys
import openai
import json
import hashlib
import logging
from rich.tree import Tree
from rich import print as rprint




load_dotenv(find_dotenv())

openai.api_key = os.environ["OPENAI_API_KEY"]

logging.getLogger("ebooklib").setLevel(logging.ERROR)


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
        "blocks",
        "operations",
        "undo",
        "get",
        "prompt",
        "tree"
    ],
    help="The action to perform ",
)


parser.add_argument("--db", help="The database file", required=False, default="promptlab.db")
parser.add_argument("--fn", help="Filename", required=False, default="test.epub")
parser.add_argument("--description", help="Description of the operations", required=False, default="")
parser.add_argument("--tag", help="Tag to filter on", required=False, default="*")
parser.add_argument("--script", help="Script to execute", required=False)
parser.add_argument("--block_id", help="Block ID to use", required=False)
parser.add_argument("--prompt", help="Prompt to use", required=False)
parser.add_argument("--model", help="Model to use", required=False, default="gpt-4")

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

def hash(txt):
    return hashlib.sha256(txt.encode('utf-8')).hexdigest()


# *****************************************************************************************
# Block operations
# *****************************************************************************************

# Write an operation to the database
def create_operation(c):
    sql = load("sql/create_operation.sql")
    arguments = " ".join(sys.argv)
    c.execute(sql, (arguments,))
    operation_id = c.lastrowid
    return operation_id

# Inserts into the blocks table and returns the block id
def create_block(c, operation_id, block, tag, parent_id):
    sql = load("sql/create_block.sql")
    c.execute(sql, (operation_id, block, tag, parent_id))
    block_id = c.lastrowid
    return block_id

# Unlike other operation, this should alsways be committed directly
def create_prompt_response(block_id,prompt_fn, prompt,arguments, elapsed_time_in_seconds, response_json):
    sql = load("sql/create_prompt_response.sql")
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    response_txt = str(response_json.choices[0].message.content)
    prompt_hash = hash(prompt)
    response_json_str = json.dumps(response_json)
    c.execute(sql, (block_id, prompt_fn, prompt, prompt_hash, response_txt, response_json_str, arguments, elapsed_time_in_seconds))
    conn.commit()
    conn.close()
    prompt_response_id = c.lastrowid
    return prompt_response_id


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
        operation_id = create_operation(c)
        # Load the file based on the filetype
        if args.fn.endswith(".epub"):
            book = epub.read_epub(args.fn, {"ignore_ncx": True})
            idx = 0
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    html = item.get_content().decode("utf-8")
                    create_block(c, operation_id, html,  item.get_name(),0)
                    idx += 1
            conn.commit()
        else:
            txt = load(args.fn)
            create_block(c, operation_id, txt, args.fn,0)
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
    if args.block_id is not None:
        blocks = fetch_blocks_by_id(args.block_id)
    else:
        blocks = fetch_blocks(args.tag)
    # Open a new connection
    conn = sqlite3.connect(args.db)
    conn.isolation_level = None
    c = conn.cursor()
    c.execute("BEGIN")
    operation_id = create_operation(c)
    try:
        for b in blocks:
            console.log("Processing block", b['tag'])
            result = execute(script, b['block'])
            if type(result) is list:
                for r in result:
                    create_block(c, operation_id, r, b['tag'], b['id'])
            elif type(result) is str:
                create_block(c, operation_id, result, b['tag'], b['id'])
            else:
                # Raise an error
                raise Exception(f"Result is not a list or string: {type(result)}")
        conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()

def action_prompt(prompt_fn):
    template = Template(load(prompt_fn))
    if args.block_id is not None:
        blocks = fetch_blocks_by_id(args.block_id)
    else:
        blocks = fetch_blocks(args.tag)
    # Apply the template to each block
    for b in blocks:
        prompt_text = template.render(block=b['block'])
        console.log("Prompting block", b['id'], b['tag'], b['block'][:40].replace("\n", " "))
        start = time.time()
        response = openai.ChatCompletion.create(
            model=args.model,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.1,
            max_tokens=500,
        )
        end = time.time()
        # Save the response to the database
        create_prompt_response(b['id'],prompt_fn, prompt_text," ".join(sys.argv), end-start, response)

        console.log("Elapsed time",end-start," -> ", response.choices[0].message.content)



def action_blocks():
    blocks = fetch_blocks(args.tag)
    table = Table(title="Blocks", header_style="bold magenta")
    table.add_column("block_id", justify="center", style="cyan")
    table.add_column("tag", justify="left")
    table.add_column("~tokens", justify="right")
    table.add_column("block", justify="left")
    total_tokens = 0
    for idx,block in enumerate(blocks):
        # Strip and \n and replace with " " for block
        tokens = len(block["block"].split(" "))
        total_tokens += tokens
        b = str(block["block"]).replace("\n", " ")
        table.add_row(
            str(block["id"]),
            block["tag"],
            '{:,}'.format(tokens),
            b[:40],
        )
    console.print(table)
    console.print(f"\n{len(blocks)} blocks with {'{:,}'.format(total_tokens)} tokens.\n")

def action_operations():
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select * from operations")
    results = c.fetchall()
    conn.close()
    table = Table(title="Operations", header_style="bold magenta")
    table.add_column("id", justify="center", style="cyan")
    table.add_column("arguments", justify="left")
    for idx,op in enumerate(results):
        table.add_row(
            str(op["id"]),
            op["arguments"]
        )
    console.print(table)
    console.print(f"\n{len(results)} operations have been performed.\n")

def action_get():
    if args.block_id is not None:
        blocks = fetch_blocks_by_id(args.block_id)
    else:
        blocks = fetch_blocks(args.tag)
    # Pull out the block element into it's own list
    out = [b['block'] for b in blocks]
    console.print("\n".join(out))

def action_tree():
    if args.block_id is not None:
        blocks = fetch_blocks_by_id(args.block_id)
    else:
        blocks = fetch_blocks(args.tag)
    # Pull out the block element into it's own list
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

if args.action == 'blocks':
    check_db(args.db)
    action_blocks()
    exit(0)

if args.action == 'operations':
    check_db(args.db)
    action_operations()
    exit(0)

if args.action == 'undo':
    check_db(args.db)
    action_undo()
    exit(0)

if args.action == 'get':
    check_db(args.db)
    action_get()
    exit(0)

if args.action == 'prompt':
    check_db(args.db)
    if args.prompt is None:
        console.log("You must provide a --prompt argument for the prompt")
        exit(1)
    action_prompt(args.prompt)
    exit(0)
    

    



