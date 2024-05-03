import argparse
import shlex
from rich.console import Console
from rich import print
from rich.table import Table
console = Console()


def print_table():
    table = Table(title="Fruit")
    table.add_column("Name", style="bold magenta")
    table.add_column("Color", style="bold cyan")
    table.add_row("Banana", "Yellow")
    table.add_row("Apple", "Green")
    table.add_row("Cherry", "Red")
    console.print(table)


parser = argparse.ArgumentParser(
    description="Mangage prommpts across long blocks of text",
    exit_on_error=False
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
        "help",
    ],
    help="The action to perform ",
)


parser.add_argument("--db", help="The database file", required=False, default="promptlab.db")
parser.add_argument("--fn", help="Filename", required=False, default="test.epub")
parser.add_argument("--description", help="Description of the groups", required=False, default="")
parser.add_argument("--tag", help="Tag to filter on", required=False, default="*")
parser.add_argument("--msg", help="Message for the operation for later search", required=False, default="*")
parser.add_argument("--script", help="Script to execute", required=False)
parser.add_argument("--block_id", help="Block ID to use", required=False)
parser.add_argument("--group_id", help="group ID to use", required=False)
parser.add_argument("--prompt", help="Prompt to use", required=False)
parser.add_argument("--model", help="Model to use", required=False, default="gpt-4")
parser.add_argument("--work", help="Work to use", required=False, default="9781098115302")



print("Welcome! Type 'exit' to quit.\n")
while True:
    cmd = input(">>> ")
    try:
        args = parser.parse_args(shlex.split(cmd))
        if args.action == "exit":
            break
        elif args.action == "init":
            print_table()
        elif args.action == "help":
            parser.print_help()
    except Exception as e:
        print(e)


