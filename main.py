import argparse
from rich.console import Console
from rich import print
from dotenv import load_dotenv, find_dotenv
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import sqlite3
import time
import shutil
import os
from jinja2 import Template
import requests

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
        "load"
    ],
    help="The action to perform ",
)


parser.add_argument("--db", help="The database file", required=False, default="promptlab.db")
parser.add_argument("--fn", help="Filename", required=False, default="test.epub")
parser.add_argument("--description", help="Description of the operations", required=False, default="")

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

# Initialize the database by reading in the schema and creating the database
def init_db():
   
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

# *****************************************************************************************
# Action operations 
# *****************************************************************************************


# Extract the contents of an epub file into the database
def load_epub(c, fn, operation_id):
    # Open the database
    book = epub.read_epub(args.fn)
    idx = 0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            html = item.get_content()
            create_block(c, operation_id, html, idx, item.get_name())
            idx += 1

# Loads a file into the database
def load_action():
    console.log("Reading file", args.fn)
    # If the load fails then we want to rollback the entire transaction
    try:
        conn = sqlite3.connect(args.db)
        c = conn.cursor()
        operation_id = create_operation(c, "read", "Loading file " + args.fn)
        # Load the file based on the filetype
        if args.fn.endswith(".epub"):
            load_epub(c, args.fn, operation_id)
            conn.commit()
        else:
            with open(args.fn, "r") as f:
                data = f.read()
            create_block(c, operation_id, data, 0, args.fn)
            conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()



# --------------------------------------------------------------------------------------------
# Begin actions
# --------------------------------------------------------------------------------------------

if args.action == 'init':
    init_db()
    console.log("Initialized database")
    exit(0)

if args.action == 'load':
    check_db(args.db)
    if args.fn is None:
        console.log("You must provide a --fn argument for the file to read")
        exit(1)

    load_action()
    

    



