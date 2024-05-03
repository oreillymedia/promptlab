import argparse
from rich.console import Console
from rich import print
from rich.table import Table
from dotenv import load_dotenv, find_dotenv
from ebooklib import epub
from bs4 import BeautifulSoup
import sqlite3
from jinja2 import Template
import sys
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
log = logging.getLogger("rich")

VERSION = "0.1.0"


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
        set_group(c, group_id)
        conn.commit()
    except Exception as e:
        console.log("Unable to process request:", e)
        conn.rollback()
    finally:
        conn.close()


parser = argparse.ArgumentParser(
    description="Mangage prommpts across long blocks of text"
)
parser.add_argument(
    "action",
    choices=[
        "transcript",
    ],
    help="The action to perform ",
)

parser.add_argument(
    "--work", help="Work to use", required=False, default="9781098115302"
)


args = parser.parse_args()

if args.action == "transcript":
    check_db(args.db)
    if args.work is None:
        console.log("You must provide a --work argument for the work to load")
        exit(1)
    action_load_transcript()
    sys.exit(0)
