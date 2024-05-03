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
from faker import Faker
import yaml

console = Console()
fake = Faker()
log = logging.getLogger("rich")

VERSION = "0.2.1"

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
    console.log(f"Loaded  API key from {home}/{ENV_FILENAME}")
    return True


# Loads a file eirher from the current directory or from the directory
# in which the script was run, which is needed when pyinstaller loads external files
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


# Convert a * wildcard to a % for sqlite3
def convert_wildcard(s):
    return s.replace("*", "%")


def generate_slug(length):
    return fake.slug()


# This function takes an array of dictionaries and then a set of transformations expressed as lambda functions
# It will iterate through the array and apply the transformation if they have matching key names.  For example:
#
# transform_by_key([{"text": "hello"}, {"text": "world"}], {"text": lambda x: x.upper()})
# will return [{"text": "HELLO"}, {"text": "WORLD"}]
#
def transform_by_key(data=[], transformations={}):
    transformed_data = []
    for d in data:
        row = {**d}
        for key, transformation in transformations.items():
            if key in row.keys():
                row[key] = transformation(row[key])
        transformed_data.append(row)
    return transformed_data


def fetch_from_db(sql, tuple):
    try:
        conn = sqlite3.connect(args.db)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(sql, tuple)
        results = c.fetchall()
        # get column names and store in a list
        column_names = [description[0] for description in c.description]
        # Unpack the sqlite row objects into a list of dictionaries
        # See this great article on this next line
        # https://nickgeorge.net/programming/python-sqlite3-extract-to-dictionary/
        unpacked = [{k: item[k] for k in item.keys()} for item in results]
        conn.close()
        return column_names, unpacked
    except Exception as e:
        console.log("[red]An error occurred on this request[/red]")
        console.log(" ".join(sys.argv))
        console.log("SQL used in this request is:\n\n", sql)
        console.log(f"\nThe following error occurred:\n\n[red]{e}[/red]\n")
        sys.exit(1)


def print_results(title, column_names, results):
    table = Table(title=title, header_style="bold magenta")
    for cn in column_names:
        table.add_column(cn)
    for row in results:
        table.add_row(*[str(row[cn]) for cn in column_names])
    console.print(table)


# *****************************************************************************************
#  Metadata
# *****************************************************************************************


def read_metadata(fn):
    txt = load_user_file(fn)
    # parse the yml file into a dictionary
    metadata = yaml.safe_load(txt)
    return metadata


# *****************************************************************************************
#  Groups
# *****************************************************************************************


def create_group(c, tag=None):
    sql = load_system_file("sql/create_group.sql")
    tag = tag if tag is not None else generate_slug(3)
    arguments = " ".join(sys.argv)
    c.execute(sql, (arguments, tag))
    group_id = c.lastrowid
    return group_id


def get_current_group():
    headers, results = fetch_from_db("select * from current_group", ())
    try:
        group_id = results[0]["id"]
    except:
        group_id = 0
    return int(group_id)


def fetch_groups():
    sql = load_system_file("sql/fetch_groups.sql")
    headers, results = fetch_from_db(sql, ())
    return results


def update_current_group(c, group_id):
    c.execute("UPDATE current_group set id = ?", (group_id,))
    return group_id


# *****************************************************************************************
#  Blocks
# *****************************************************************************************


def create_block(c, group_id, block, tag, parent_id):
    sql = load_system_file("sql/create_block.sql")
    token_count = len(block.split(" "))
    c.execute(sql, (group_id, block, tag, parent_id, token_count))
    block_id = c.lastrowid
    return block_id


# fetch blocks and apply where clause if it exists
# TODO: something arouns sql injection here. there is probbaly a python library
def fetch_blocks(tag=None, latest=True):
    sql = load_system_file("sql/v_current_blocks.sql")
    if args.where is not None:
        sql += " where " + args.where
    return fetch_from_db(sql, ())


# *****************************************************************************************
#  Prompts
# *****************************************************************************************


def create_prompt_response(
    prompt_log_id, block_id, prompt_text, response_txt, elapsed_time_in_seconds
):
    sql = load_system_file("sql/create_prompt_response.sql")
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
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
    tag = args.prompt_tag if args.prompt_tag is not None else generate_slug(3)
    c.execute(sql, (prompt_fn, prompt, arguments, tag))
    conn.commit()
    conn.close()
    prompt_log_id = c.lastrowid
    return prompt_log_id, tag


def response_already_exists(prompt_text):
    headers, result = fetch_from_db(
        "select * from prompt_responses where prompt_hash like ?", (hash(prompt_text),)
    )
    return len(result) > 0


def fetch_prompts():
    sql = load_system_file("sql/v_current_prompts.sql")
    if args.where is not None:
        sql += " where " + args.where
    return fetch_from_db(sql, ())


def fetch_prompts_old():
    tag = convert_wildcard(args.tag) if args.tag is not None else "%"
    sql = load_system_file("sql/fetch_prompts.sql.jinja")
    template = Template(sql)
    where_clause = ""
    tuple = ()
    if args.block_id is not None:
        where_clause = "b.id = ?"
        tuple = (int(args.block_id),)
    else:
        where_clause = "search_field like ?"
        tuple = (tag,)
    sql = template.render(where_clause=where_clause)
    headers, results = fetch_from_db(sql, tuple)
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
        group_id = create_group(c, args.group_tag)
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
        group_id = create_group(c, args.group_tag)
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


def action_transfer_prompts_to_blocks(prompt_tag):
    console.log("Creating blocks from prompt tag", prompt_tag)
    # If the load fails then we want to rollback the entire transaction
    try:
        conn = sqlite3.connect(args.db)
        conn.isolation_level = None
        c = conn.cursor()
        c.execute("BEGIN")
        group_id = create_group(c, args.group_tag)
        # Load the prompt data
        sql = load_system_file("sql/load_blocks_from_prompts.sql")
        headers, results = fetch_from_db(sql, (prompt_tag,))
        for idx, p in enumerate(results):
            create_block(c, group_id, p["block"], p["tag"], p["parent"])
        update_current_group(c, group_id)
        conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()


# Takes prompts and converts them to metadata under the supplied key
def action_transfer_prompts_to_metadata(prompt_tag, metadata_key):
    sql = load_system_file("sql/fetch_prompts_action.sql")
    header, results = fetch_from_db(sql, (prompt_tag,))
    try:
        sql = load_system_file("sql/create_metadata.sql")
        conn = sqlite3.connect(args.db)
        conn.isolation_level = None
        c = conn.cursor()
        c.execute("BEGIN")
        for r in results:
            c.execute(sql, (r["block_id"], metadata_key, r["response"]))
        conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()


def action_transform(transformation):
    # Fetch the block or blocks to use
    headers, blocks = fetch_blocks()
    # Open a new connection
    conn = sqlite3.connect(args.db)
    conn.isolation_level = None
    c = conn.cursor()
    c.execute("BEGIN")
    group_id = create_group(c, args.group_tag)
    try:
        for b in blocks:
            console.log("Processing block", b["block_tag"])
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
                    raise Exception(f"Unknown transformation {args.transformation}")
            # If the result is a list, then create a block for each element
            if type(result) is list:
                for r in result:
                    create_block(c, group_id, r, b["block_tag"], b["block_id"])
            elif type(result) is str:
                create_block(c, group_id, result, b["block_tag"], b["block_id"])
            else:
                # Raise an error
                raise Exception(f"Result is not a list or string: {type(result)}")
        update_current_group(c, group_id)
        conn.commit()
    except Exception as e:
        conn.rollback()
        console.log(f"[red]The following error occurred: {e}[/red]")
        sys.exit(1)
    finally:
        conn.close()


def action_prompt(prompt_fn):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    prompt = load_user_file(prompt_fn)
    metadata = {}
    if args.globals is not None:
        metadata = read_metadata(args.globals)
    template = Template(prompt)
    headers, blocks = fetch_blocks()
    # Apply the template to each block
    prompt_log_id, prompt_tag = create_prompt_log(prompt_fn, prompt)
    idx = 1
    for b in blocks:
        prompt_text = template.render(block=b["block"], **metadata)
        if response_already_exists(prompt_text):
            console.log(
                f"({idx}/{len(blocks)}) Prompt already exists for",
                b["block_id"],
                b["block_tag"],
                b["block"][:40].replace("\n", " "),
            )
            idx += 1
            continue
        console.log(
            f"({idx}/{len(blocks)}) Prompting block",
            b["block_id"],
            b["block_tag"],
            b["block"][:40].replace("\n", " "),
        )
        start = time.time()
        response = "TBD"
        if args.fake:
            response_txt = fake.text(500)
        else:
            response = openai.ChatCompletion.create(
                model=args.model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.1,
                max_tokens=1000,
            )
            response_txt = str(response.choices[0].message.content)
        idx += 1
        end = time.time()
        # Save the response to the database
        create_prompt_response(
            prompt_log_id, b["block_id"], prompt_text, response_txt, end - start
        )
        console.log(
            "Elapsed time", end - start, " -> ", response_txt[:40].replace("\n", " ")
        )
    console.log(
        f"\nPrompt response saved with id {prompt_log_id} and prompt_tag {prompt_tag}"
    )


def action_filter():
    console.log("Filtering blocks")
    # Fetch the block or blocks to use
    headers, blocks = fetch_blocks()
    # Open a new connection
    conn = sqlite3.connect(args.db)
    conn.isolation_level = None
    c = conn.cursor()
    c.execute("BEGIN")
    group_id = create_group(c, args.group_tag)
    try:
        for b in blocks:
            console.log("Processing block", b["block_tag"])
            create_block(c, group_id, b["block"], b["block_tag"], b["block_id"])
        update_current_group(c, group_id)
        conn.commit()
    except Exception as e:
        conn.rollback()
        console.log(f"[red]The following error occurred: {e}[/red]")
        sys.exit(1)
    finally:
        conn.close()


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
# Reporting functions -- these mostly just fetch data from the database and print it
# *****************************************************************************************
def action_blocks():
    columns, results = fetch_blocks()
    # add token count in the block column to the results

    # use lise comprehension to sum up the results["token_count"] to get the total tokens
    total_tokens = sum([r["token_count"] for r in results])

    # Transform the results to make them more readable
    results = transform_by_key(
        results,
        {
            "block": lambda x: x[:40].replace("\n", " "),
            "token_count": lambda x: "{:,}".format(x),
        },
    )
    print_results("Current Blocks", columns, results)
    console.print(f"\n{len(results)} blocks with {'{:,}'.format(total_tokens)} tokens.")
    console.print(f"Current group id = {get_current_group()}\n")
    console.print("The following fields available in --where clause:", columns)


def action_groups():
    sql = load_system_file("sql/fetch_groups.sql")
    headers, results = fetch_from_db(sql, ())
    print_results("Groups", headers, results)
    console.print(f"\n{len(results)} group(s) in total")
    console.print(f"Current group_id: {get_current_group()}\n")


def action_prompt_log(prompt_tag):
    sql = load_system_file("sql/fetch_prompt_log.sql")
    tag = convert_wildcard(prompt_tag) if prompt_tag is not None else "%"
    console.log("Fetching prompt logs for tag", tag)
    columns, results = fetch_from_db(sql, (tag,))
    print_results("Prompt Logs", columns, results)


def action_prompts():
    sql = load_system_file("sql/v_current_prompts.sql")
    if args.where is not None:
        sql += " where " + args.where
    columns, results = fetch_from_db(sql, ())
    results = transform_by_key(
        results,
        {
            "response": lambda x: x[:40].replace("\n", " "),
            "elapsed_time_in_seconds": lambda x: f"{x:.2f}",
        },
    )
    print_results("Prompts", columns, results)
    console.print(f"\n{len(results)} prompts in total")
    console.print("The following fields available in --where clause:", columns)


def action_dump_blocks():
    headers, blocks = fetch_blocks()
    # Pull out the block element into it's own list
    out = [b["block"] for b in blocks]
    console.print(get_delimiter().join(out))


def action_dump_prompts():
    prompts = fetch_prompts()
    # Pull out the block element into it's own list
    out = [p["response"] for p in prompts]
    console.print(get_delimiter().join(out))


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
        "load-prompts",
        "dump-blocks",
        "dump-prompts",
        "transform",
        "groups",
        "blocks",
        "prompt",
        "prompts",
        "prompt-log",
        "set-group",
        "version",
        "set-openai-key",
        "transfer-prompts",
        "filter",
    ],
    help="The action to perform ",
)


parser.add_argument(
    "--db", help="The database file", required=False, default="promptlab.db"
)
parser.add_argument("--fn", help="Filename", required=False)
parser.add_argument(
    "--description", help="Description of the groups", required=False, default=""
)
parser.add_argument("--prompt_tag", help="Tag to filter on", required=False)
parser.add_argument("--group_tag", help="Tag to filter on", required=False)
parser.add_argument("--tag", help="Tag to filter on", required=False)

parser.add_argument(
    "--where", help="SQLITE Where clause to use to select blocks", required=False
)

parser.add_argument(
    "--globals", help="Name of the file with global metadata", required=False
)

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

parser.add_argument(
    "--fake",
    help="Generate fake prompt response data (mostly for testing)",
    required=False,
    default=False,
    action=argparse.BooleanOptionalAction,
)

parser.add_argument(
    "--to",
    help="Where to transfer prompts",
    choices=["metadata", "blocks"],
    required=False,
    default="metadata",
)

parser.add_argument(
    "--metadata_key",
    help="Name of metadata key; this will match the name in a prompt template",
    required=False,
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

if args.action == "load-transcript":
    check_db(args.db)
    if args.work is None:
        console.log("You must provide a --work argument for the work to load")
        exit(1)
    action_load_transcript()
    sys.exit(0)

if args.action == "load-prompts":
    check_db(args.db)
    if args.fn is None:
        console.log("You must provide a --fn argument for the file to read")
        exit(1)
    if args.prompt_tag is None:
        console.log("You must provide a --prompt_tag argument for the prompt tag")
        exit(1)
    action_load_prompts(args.prompt_tag)
    sys.exit(0)

if args.action == "transform":
    check_db(args.db)
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
    console.log(args.fn)
    if args.fn is None:
        console.log("You must provide a --fn argument for the prompt")
        sys.exit(1)
    if load_env() is False:
        action_set_openai_key()
        load_env()
    action_prompt(args.fn)
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

if args.action == "prompt-log":
    check_db(args.db)
    action_prompt_log(args.prompt_tag)
    sys.exit(0)


if args.action == "version":
    console.log("Version", VERSION)
    sys.exit(0)

if args.action == "set-openai-key":
    action_set_openai_key()
    sys.exit(0)

if args.action == "metadata":
    if args.globals is None:
        console.log("You must provide a --globals argument for the metadata file")
        sys.exit(1)
    metadata = read_metadata(args.globals)
    console.log(metadata)
    sys.exit(0)

if args.action == "transfer-prompts":
    check_db(args.db)
    if args.prompt_tag is None:
        console.log("You must provide a --prompt_tag argument for the prompt tag")
        exit(1)
    if args.to == "metadata" and args.metadata_key is None:
        console.log("You must provide a --metadata_key argument for the metadata key")
        exit(1)
    if args.to == "metadata":
        action_transfer_prompts_to_metadata(args.prompt_tag, args.metadata_key)
    elif args.to == "blocks":
        action_transfer_prompts_to_blocks(args.prompt_tag)
    else:
        console.log("Unknown transfer target", args.to)
        sys.exit(1)

if args.action == "filter":
    check_db(args.db)
    if args.where is None:
        console.log("You must provide a --where clause for the filter")
        exit(1)
    action_filter()
    sys.exit(0)
