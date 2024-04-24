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
import re
import sys
import openai
import json
import hashlib
import logging
import requests
import glob
from slugify import slugify
from transformations import *
import os
from pathlib import Path
from coolname import generate_slug


console = Console()
log = logging.getLogger("rich")

VERSION = "0.2.0"

ENV_FILENAME = ".promptlab"


# *****************************************************************************************
# Utiltiy functions
# *****************************************************************************************
# If the db exists; if not, print error and exit.  Otherwise sqlite silently create a new file.
def check_db(fn):
    if not os.path.isfile(fn):
        console.log(
            "Database file",
            fn,
            "does not exist.  Check the filename or run init to create a new database.",
        )
        exit(1)


# Check if the .promptlab file exists in the home directory
def load_env():
    home = str(Path.home())
    if not os.path.isfile(home + "/" + ENV_FILENAME):
        return False
    load_dotenv(home + "/" + ENV_FILENAME)
    console.log(f"Loaded OpenAI API key from {home}/{ENV_FILENAME}")
    return True


def load_file(fn, config=False):
    if config:
        # find filepath for where the script is actually running
        script_path = os.path.dirname(os.path.realpath(__file__))
        # Join the filename with the script path
        fn = os.path.join(script_path, fn)
    # Check if the file exists
    if not os.path.isfile(fn):
        raise Exception(f"File does not exist:{fn}")
    # Load and return the file
    with open(fn, "r") as f:
        data = f.read()
    return data


def load_system_file(fn):
    return load_file(fn, True)


def load_user_file(fn):
    return load_file(fn, False)


def hash(txt):
    return str(hashlib.sha256(txt.encode("utf-8")).hexdigest())


def get_delimiter():
    d = args.delimiter
    d = d.replace(r"\n", "\n")
    return d


# *****************************************************************************************
#  Groups
# *****************************************************************************************


def create_group(c):
    sql = load_system_file("sql/create_group.sql")
    arguments = " ".join(sys.argv)
    tag = args.tag if args.tag is not None else generate_slug(3)
    c.execute(sql, (arguments, tag))
    group_id = c.lastrowid
    return group_id


def get_current_group():
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select * from current_group")
    group_id = c.fetchone()[0]
    conn.close()
    return int(group_id)


def fetch_groups():
    sql = load_system_file("sql/fetch_groups.sql")
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


# *****************************************************************************************
#  Blocks
# *****************************************************************************************


def create_block(c, group_id, block, tag, parent_id):
    sql = load_system_file("sql/create_block.sql")
    c.execute(sql, (group_id, block, tag, parent_id))
    block_id = c.lastrowid
    return block_id


def fetch_blocks(tag, latest=True):
    # Replace the * with a pct, which is what sqlite3 requires for wildcards
    tag = tag if tag is not None else "*"
    tag = tag.replace("*", "%")
    if latest:
        sql = load_system_file("sql/fetch_latest_blocks.sql")
    else:
        sql = load_system_file("sql/fetch_blocks.sql")
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
    sql = load_system_file("sql/fetch_block_by_id.sql")
    # Grab the data
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(sql, (id,))
    results = c.fetchall()
    conn.close()
    return results


# *****************************************************************************************
#  Prompts
# *****************************************************************************************


def create_prompt_response(
    prompt_log_id, block_id, prompt_text, response, elapsed_time_in_seconds
):
    sql = load_system_file("sql/create_prompt_response.sql")
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    response_txt = str(response.choices[0].message.content)
    c.execute(
        sql,
        (
            prompt_log_id,
            block_id,
            hash(prompt_text),
            response_txt,
            elapsed_time_in_seconds,
        ),
    )
    # Unlike other group, this should alsways be committed directly
    conn.commit()
    conn.close()
    prompt_response_id = c.lastrowid
    return prompt_response_id


def create_prompt_log(prompt_fn, prompt):
    sql = load_system_file("sql/create_prompt_log.sql")
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    arguments = " ".join(sys.argv)
    c.execute(sql, (prompt_fn, prompt, arguments))
    conn.commit()
    conn.close()
    prompt_log_id = c.lastrowid
    return prompt_log_id


def response_already_exists(prompt_text):
    sql = "select * from prompt_responses where prompt_hash like ?"
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    c.execute(sql, (hash(prompt_text),))
    result = c.fetchone()
    conn.close()
    return result is not None


def fetch_prompts():
    sql = load_system_file("sql/fetch_prompts.sql.jinja")
    template = Template(sql)
    where_clause = ""
    tuple = ()
    if args.block_id is not None:
        where_clause = "b.id = ?"
        tuple = (int(args.block_id),)
    elif args.tag is not None:
        where_clause = "search_field like ?"
        tuple = (args.tag.replace("*", "%"),)
    sql = template.render(where_clause=where_clause)
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(sql, tuple)
    results = c.fetchall()
    conn.close()
    return results


# *****************************************************************************************
# Functions related to fetching a transcript
# *****************************************************************************************


def fetch_url(url):
    console.log("[bold]Fetching... [/]: [italic]" + url + "[/]")
    r = requests.get(url)
    return r.json()


# Fetch the table of contents given a work
def fetch_toc_url(work):
    url = f"https://learning.oreilly.com/api/v1/book/{work}/toc/"
    return url


# Fetch the transcript given a work and a fragment
def fetch_transcript_url(work, fragment):
    url = f"https://learning.oreilly.com/api/v1/book/{work}/chapter-content/{fragment}"
    return url


# Reads in a table of contents and flattens it into a list
def flatten_toc(toc, out=[], depth=0):
    for child in toc:
        # deep Copy the cild into a new variable
        rec = {
            "id": child["id"],
            "title": child["label"],
            "url": child["url"],
            "metadata": {
                "full_path": child["full_path"],
                "depth": child["depth"] + depth,
            },
        }
        out.append(rec)
        if "children" in child:
            flatten_toc(child["children"], out, depth + 1)
    return out


# Fetch the transcript given a URL and return just the text
def fetch_transcript_by_url(url):
    console.log("[bold]Parsing... [/]: [italic]" + url + "[/]")
    r = requests.get(url)
    raw = r.text
    soup = BeautifulSoup(raw, "html.parser")
    transcript = ""
    for p in soup.select(".transcript p"):
        text = p.select_one(".text").get_text()
        transcript += text + " "
    return transcript


def action_load_transcript():

    # Fetch the work's table of contents
    toc_url = fetch_toc_url(args.work)
    toc = fetch_url(toc_url)
    flattened_toc = flatten_toc(toc)
    # Grab the transcript for each work and store it as metadata
    try:
        conn = sqlite3.connect(args.db)
        conn.isolation_level = None
        c = conn.cursor()
        c.execute("BEGIN")
        group_id = create_group(c)
        for idx, t in enumerate(flattened_toc):
            url = fetch_transcript_url(args.work, t["metadata"]["full_path"])
            transcript = fetch_transcript_by_url(url)
            level = "#"
            if t["metadata"]["depth"] > 1:
                level = "##"
            md = f"{level} {t['title']}\n\n{transcript}"
            # format idx to 3 digits
            tag = args.work + "-" + str(idx + 1).zfill(3) + "-" + slugify(t["title"])
            create_block(c, group_id, md, tag, 0)
        update_current_group(c, group_id)
        conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()


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
    sql = load_system_file("sql/schema.sql")
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
                    create_block(c, group_id, html, item.get_name(), 0)
                    idx += 1
            update_current_group(c, group_id)
            conn.commit()
        else:
            files = glob.glob(args.fn)
            idx = 0
            for f in files:
                txt = load_user_file(f)
                create_block(c, group_id, txt, f, idx)
                idx += 1
            update_current_group(c, group_id)
            conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()


def action_transform(transformation):
    # Fetch the block or blocks to use
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
            console.log("Processing block", b["tag"])
            # Apply the transformation to the block
            match transformation:
                case "token-split":
                    result = transformation_token_split(b["block"])
                case "clean-epub":
                    result = transformation_clean_epub(b["block"])
                case "html-h1-split":
                    result = transformation_html_heading_split(b["block"], ["h1"])
                case "html-h2-split":
                    result = transformation_html_heading_split(b["block"], ["h1", "h2"])
                case "html2md":
                    result = transformation_html2md(b["block"])
                case "html2txt":
                    result = transformation_html2txt(b["block"])
                case "new-line-split":
                    result = transformation_newline_split(b["block"])
                case _:
                    console.log("Unknown transformation", args.transformation)
                    sys.exit(1)
            # If the result is a list, then create a block for each element
            if type(result) is list:
                for r in result:
                    create_block(c, group_id, r, b["tag"], b["id"])
            elif type(result) is str:
                create_block(c, group_id, result, b["tag"], b["id"])
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
    openai.api_key = os.environ["OPENAI_API_KEY"]
    prompt = load_user_file(prompt_fn)
    template = Template(prompt)
    if args.block_id is not None:
        blocks = fetch_blocks_by_id(args.block_id)
    else:
        blocks = fetch_blocks(args.tag)
    # Apply the template to each block
    prompt_log_id = create_prompt_log(prompt_fn, prompt)
    idx = 1
    for b in blocks:
        prompt_text = template.render(block=b["block"])
        if response_already_exists(prompt_text):
            console.log(
                f"({idx}/{len(blocks)}) Prompt already exists for",
                b["id"],
                b["tag"],
                b["block"][:40].replace("\n", " "),
            )
            idx += 1
            continue
        console.log(
            f"({idx}/{len(blocks)}) Prompting block",
            b["id"],
            b["tag"],
            b["block"][:40].replace("\n", " "),
        )
        start = time.time()
        response = openai.ChatCompletion.create(
            model=args.model,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.1,
            max_tokens=1000,
        )
        idx += 1
        end = time.time()
        # Save the response to the database
        create_prompt_response(
            prompt_log_id, b["id"], prompt_text, response, end - start
        )
        console.log(
            "Elapsed time", end - start, " -> ", response.choices[0].message.content
        )


def action_blocks():
    blocks = []
    if args.block_id is not None:
        blocks = fetch_blocks_by_id(args.block_id)
    else:
        blocks = fetch_blocks(args.tag)
    current_group = get_current_group()
    table = Table(
        title=f"Blocks for group id {current_group}", header_style="bold magenta"
    )
    table.add_column("block_id", justify="center", style="cyan")
    table.add_column("tag", justify="left")
    table.add_column("~tokens", justify="right")
    table.add_column("block", justify="left")
    total_tokens = 0
    for idx, block in enumerate(blocks):
        # Strip and \n and replace with " " for block
        b = str(block["block"]).replace("\n", " ")
        tokens = len(b.split(" "))
        total_tokens += tokens
        table.add_row(
            str(block["id"]),
            block["tag"],
            "{:,}".format(tokens),
            b[:40] + "...",
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
                f"[bold][red]{op['block_count']}",
            )
        else:
            table.add_row(str(op["id"]), op["arguments"], str(op["block_count"]))
    console.print(table)
    console.print(f"\nCurrent group_id: {current_group_id}")
    console.print(f"{len(results)} group(s) in total\n")


def action_prompts():
    prompts = fetch_prompts()
    table = Table(title=f"Prompts that match your query", header_style="bold magenta")
    table.add_column("prompt_id", justify="center", style="cyan")
    table.add_column("block_id", justify="center", style="cyan")
    table.add_column("search_field", justify="left")
    table.add_column("block", justify="left")
    for op in prompts:
        # Convert the print statement to a rich table
        table.add_row(
            str(op["prompt_response_id"]),
            str(op["block_id"]),
            op["search_field"],
            op["block"].replace("\n", " ")[:50],
        )
    console.print(table)


def action_dump_blocks():
    if args.block_id is not None:
        blocks = fetch_blocks_by_id(args.block_id)
    else:
        blocks = fetch_blocks(args.tag)
    # Pull out the block element into it's own list
    out = [b["block"] for b in blocks]
    console.print(get_delimiter().join(out))


def action_dump_prompts():
    prompts = fetch_prompts()
    # Pull out the block element into it's own list
    out = [p["response"] for p in prompts]
    console.print(get_delimiter().join(out))


def action_set_openai_key():
    home = str(Path.home())
    # get user input for openai key
    openai_key = input("Enter your OpenAI API key: ")
    # write the key to the .promptlab file
    console.log(f"Missing openai credentials in file {home}/{ENV_FILENAME}.")
    with open(home + "/" + ENV_FILENAME, "w") as f:
        f.write(f"OPENAI_API_KEY={openai_key}")
    console.log(f"API key set successfully and saved in {home}/{ENV_FILENAME}")


# *****************************************************************************************
# Define commandline flags, arguments, and the functions that love them
# *****************************************************************************************

parser = argparse.ArgumentParser(
    description="Mangage prommpts across long blocks of text"
)
parser.add_argument(
    "action",
    choices=[
        "init",
        "load",
        "load-transcript",
        "dump-blocks",
        "dump-prompts",
        "group",
        "groups",
        "blocks",
        "prompt",
        "prompts",
        "set-group",
        "version",
        "set-openai-key",
    ],
    help="The action to perform ",
)


parser.add_argument(
    "--db", help="The database file", required=False, default="promptlab.db"
)
parser.add_argument("--fn", help="Filename", required=False, default="test.epub")
parser.add_argument(
    "--description", help="Description of the groups", required=False, default=""
)
parser.add_argument("--tag", help="Tag to filter on", required=False)
parser.add_argument(
    "--msg",
    help="Message for the operation for later search",
    required=False,
    default="*",
)


parser.add_argument(
    "--transformation",
    help="Transformation to use: token-split | clean-epub | html-h1-split | html-h2-split | html2md | html2txt | new-line-split",
    required=False,
)
parser.add_argument("--block_id", help="Block ID to use", required=False)
parser.add_argument("--group_id", help="Group ID to use", required=False)
parser.add_argument("--prompt", help="Prompt to use", required=False)
parser.add_argument("--model", help="Model to use", required=False, default="gpt-4")
parser.add_argument(
    "--work", help="Work to use", required=False, default="9781098115302"
)
parser.add_argument(
    "--delimiter",
    help="Delimiter to use when dumping prompts",
    required=False,
    default="\n\n",
)

args = parser.parse_args()

if args.action == "init":
    action_init()
    console.log("Initialized database")
    sys.exit(0)

if args.action == "load":
    check_db(args.db)
    if args.fn is None:
        console.log("You must provide a --fn argument for the file to read")
        exit(1)
    action_load()

if args.action == "group":
    check_db(args.db)
    if args.fn is None:
        console.log("You must provide a --fn argument for the file to read")
        sys.exit(1)
    if args.transformation is None:
        console.log("You must provide a --transformation argument to use")
        sys.exit(1)
    action_transform(args.transformation)

if args.action == "blocks":
    check_db(args.db)
    action_blocks()
    sys.exit(0)

if args.action == "groups":
    check_db(args.db)
    action_groups()
    sys.exit(0)

if args.action == "dump-blocks":
    check_db(args.db)
    action_dump_blocks()
    sys.exit(0)

if args.action == "dump-prompts":
    check_db(args.db)
    action_dump_prompts()
    sys.exit(0)

if args.action == "prompt":
    check_db(args.db)
    if args.prompt is None:
        console.log("You must provide a --prompt argument for the prompt")
        sys.exit(1)
    if load_env() is False:
        action_set_openai_key()
        load_env()
    action_prompt(args.prompt)
    sys.exit(0)

if args.action == "set-group":
    check_db(args.db)
    if args.group_id is None:
        console.log("You must provide a --group_id argument for the group")
        exit(1)
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    update_current_group(c, args.group_id)
    conn.commit()
    conn.close()

if args.action == "prompts":
    check_db(args.db)
    action_prompts()
    sys.exit(0)

if args.action == "load-transcript":
    check_db(args.db)
    if args.work is None:
        console.log("You must provide a --work argument for the work to load")
        exit(1)
    action_load_transcript()
    sys.exit(0)

if args.action == "version":
    console.log("Version", VERSION)
    sys.exit(0)

if args.action == "set-openai-key":
    action_set_openai_key()
    sys.exit(0)
