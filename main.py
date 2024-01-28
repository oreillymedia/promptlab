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
        "group",
        "blocks",
        "groups",
        "get",
        "prompt",
        "set-group"
    ],
    help="The action to perform ",
)


parser.add_argument("--db", help="The database file", required=False, default="promptlab.db")
parser.add_argument("--fn", help="Filename", required=False, default="test.epub")
parser.add_argument("--description", help="Description of the groups", required=False, default="")
parser.add_argument("--tag", help="Tag to filter on", required=False, default="*")
parser.add_argument("--script", help="Script to execute", required=False)
parser.add_argument("--block_id", help="Block ID to use", required=False)
parser.add_argument("--group_id", help="group ID to use", required=False)
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
# Block groups
# *****************************************************************************************

# Write an group to the database
def create_group(c):
    sql = load("sql/create_group.sql")
    arguments = " ".join(sys.argv)
    c.execute(sql, (arguments,))
    group_id = c.lastrowid
    return group_id

def get_current_group():
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select id from current_group")
    group_id = c.fetchone()[0]  
    conn.close()      
    return int(group_id)

def fetch_groups():
    sql = load("sql/fetch_groups.sql")
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()
    conn.close()
    return results

def update_current_group(c, group_id):
    c.execute("UPDATE current_group set id = ?", (group_id,))
    return group_id

# Inserts into the blocks table and returns the block id
def create_block(c, group_id, block, tag, parent_id):
    sql = load("sql/create_block.sql")
    c.execute(sql, (group_id, block, tag, parent_id))
    block_id = c.lastrowid
    return block_id

# Unlike other group, this should alsways be committed directly
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
# Action groups 
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
        group_id = create_group(c)
        # Load the file based on the filetype
        if args.fn.endswith(".epub"):
            book = epub.read_epub(args.fn, {"ignore_ncx": True})
            idx = 0
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    html = item.get_content().decode("utf-8")
                    create_block(c, group_id, html,  item.get_name(),0)
                    idx += 1
            update_current_group(c, group_id)
            conn.commit()
        else:
            txt = load(args.fn)
            create_block(c, group_id, txt, args.fn,0)
            update_current_group(c, group_id)
            conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
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
    group_id = create_group(c)
    try:
        for b in blocks:
            console.log("Processing block", b['tag'])
            result = execute(script, b['block'])
            if type(result) is list:
                for r in result:
                    create_block(c, group_id, r, b['tag'], b['id'])
            elif type(result) is str:
                create_block(c, group_id, result, b['tag'], b['id'])
            else:
                # Raise an error
                raise Exception(f"Result is not a list or string: {type(result)}")
        update_current_group(c, group_id)
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
    current_group = get_current_group()
    table = Table(title=f"Blocks for group id {current_group}", header_style="bold magenta")
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
    console.print(f"\n{len(blocks)} blocks with {'{:,}'.format(total_tokens)} tokens.")
    console.print(f"Current group id = {current_group}\n")

def action_groups():
    current_group_id = get_current_group()
    results = fetch_groups()
    table = Table(title="groups", header_style="bold magenta")
    table.add_column("id", justify="center")
    table.add_column("arguments", justify="left")
    table.add_column("blocks", justify="left")
    for op in results:
        if op["id"] == current_group_id:   
            table.add_row(
                f"[bold][red]{op['id']}",
                f"[bold][red]{op['arguments']}",
                f"[bold][red]{op['block_count']}"
            )
        else:
            table.add_row(
                str(op["id"]),
                op["arguments"],
                str(op["block_count"])
            )
    console.print(table)
    console.print(f"\n{len(results)} groups.\n")
    

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

if args.action =='group':
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

if args.action == 'groups':
    check_db(args.db)
    action_groups()
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

if args.action == 'set-group':
    check_db(args.db)
    if args.group_id is None:
        console.log("You must provide a --group_id argument for the group")
        exit(1)
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    update_current_group(c, args.group_id)
    conn.commit()
    conn.close()
    

    



