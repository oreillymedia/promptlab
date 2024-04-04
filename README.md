# Prompt Lab

Promptlab has 3 key concepts:

- _Blocks_. Blocks of text of any length or format (text, HTML, markdown, etc).

- _Groups_. A group of blocks created by running a script. Examples include: transforming text from one format to another (e.g., HTML to Markdown) or splitting a long block into several smaller ones (e.g. breaking a long HTML into sections hased on heading tags like H1 or H2). Some scripts are included in the repo, but users can also write their own.

- _Prompts_. The result from a prompt template applied against a block and sent to OpenAI's LLM. Promptlab combines your template (in Jinija2 format) with the given block, sends it to the LLM, and stores the result.

A few other important ideas:

- _IDs_. Each element has a unique ID. IDs are assigned automatically when the element is created. IDs are used to refer to specific blocks, groups, or prompts.

- _Load_ -- the process of reading a file or EPUB archive and creating a group and a corresponding block (in the case of a single file) or set of blocks (in the case of an epub)

- _Tags_. Tags are used to group blocks on an initial load. For example, if you load a tag from a file, it will be tagged with the file's name. It you load an EPUB, each block will be tagged with the chapter name. Tags are carried forward across group actions. So, if you split a block into 3 smaller blocks, all 3 will have the same tag as the original block.

- _Init_ -- Creating a new, empty SQLITE database to store the content. By default, the database is named `promptlab.db`.

- [SQLite3](https://www.sqlite.org/index.html). Promptlab uses SQLite3 as the database. The database is created automatically when you run `init`. You can use the [SQLite3 command line tool](https://www.sqlite.org/cli.html) to inspect the database directly or use a GUI like [DB Browser for SQLite](https://sqlitebrowser.org/).

# Installation

You'll need Python 3.10.9 or later. Clone this repo and run `pip install -r requirements.txt` to install the dependencies.

# Usage

## Initialize and empty database

Creates an empty database. If no db is provided, the default is `promptlab.db`.

```
python main.py init --db=database.db
```

## Loading initial text

Load an initial file. The file can be either a single file or an EPUB. A single file is loaded into a new group and given a single block.

```
python main.py load --fn=example.html
```

Loading an EPUB will create a group for each chapter and a block for each chapter:

```
python main.py load --fn=example.epub
```

You can also load transcripts of a given work:

```
python main.py load-transcript --work=9781098115302
```

When doing this, the tag will include the segment name in the tag when pulling down a transcript. The tag now looks like this "9781098115302-001-introduction".

```
│    67    │ 9781098115302-000-introduction                                         │     224 │ # Introduction  Hi. │    68    │ 9781098115302-001-product-development-loop                             │     720 │ # Product Development │    69    │ 9781098115302-002-product-development-loop-introduction                │     721 │ ## Product
```

So, you will need to use a whildcard you're searching for all the works in a transcript.

## Working with Groups

Groups are sets of related blocks tied together by the original filename. For example, you might have an initial group of blocks representing 10 chapters in a book, a group that transforms those chapters into markdown, and a group that splits the chapters into smaller blocks.

### Creating groups

You create a group by running a script against the blocks in the current group. This creates a new group with the transformed blocks as members. The original group is not modified.

For example, if you load a new file you'll get a new group and a single block with the file's contents. You can then run a script to split the block into smaller blocks. The result will be a new group with the smaller blocks. The original group will still have the single block. You can set which group you want to use using the `set-group` command; think of this as a kind of `cd` in a file system.

The following scripts are included in the `transformations` directory:

- `clean-epub.py` -- Removes much of the extraneous HTML from an EPUB, leaving mostly just the paragraph and header tags that are useful for training an LLM.
- `html-section-split.py` -- Splits an HTML block into smaller blocks based on the heading tags (H1, H2). Useful for breaking up larger chapter files into smaller sections that will fit within the 8k context window of the LLM.
- `html2md.py` -- Converts an HTML block to markdown.

To run a script, use the `group` command and provide the script name using the `--script` option:

```

python main.py group --script=transformations/html-section-split.py

```

### Listing groups

To list all groups, use the `groups` command:

```

python main.py groups

```

The results will look something like this:

```

┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ id ┃ arguments ┃ blocks ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1 │ main.py load │ 26 │
│ 2 │ main.py group --script=transformations/clean_epub.py │ 26 │
│ 3 │ main.py group --script=transformations/soup-split.py │ 205 │
│ 4 │ main.py group --script=transformations/html2md.py │ 205 │
└────┴──────────────────────────────────────────────────────┴────────┘

Current group_id: 4
4 group(s) in total

```

### Setting the current group

To set the current group, use the `set-group` command:

```
python main.py set-group --group_id=1
```

### Writing your own group scripts

In addition to using the scripts in the `transformation` directory, you can also write your own custom scripts to make groups. A script accepts an initial single block and can return a single block or a list of blocks. For example, here is a script that will capitalize all the letters in a block:

```python
def main(b):
    return b.upper()

result =  main(block)
```

Here's an example that will break the block into blocks of 5,000 characters each:

```python
# Split a block into tokens of length N
def main(b):
    N = 5000
    res = []
    tokens = b.split()
    for i in range(0, len(tokens), N):
        res.append(' '.join(tokens[i:i+N]))
    return res

result =  main(block)
```

## Blocks

Blocks are chunks of text that belong to a group. If you think of a group as a chapter, then blocks are like sections or paragraphs. Blocks are created by running a script against the blocks in the current group. The original group is not modified.

### Listing blocks

Use the `blocks` command to list all blocks in the current group:

```
python main.py blocks
```

Since many goups will have lots of blocks by the time you're done transforming and splitting them into chunks, you can use the `--tag` option to filter the results. For example, if you want to see all the blocks that were created from a specific file, you can use the `--tag` option to filter the results. Note that you can use a wilcard `*` in the tag name. For example, if you want to see all the blocks that were created from a file named `part03.html`, you can use the following command:

```
$ python main.py blocks --tag=part03*

                             Blocks for group id 4
┏━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ block_id ┃ tag         ┃ ~tokens ┃ block                                    ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│   417    │ part03.html │     212 │ #  Part III. Derived Data   In Parts  [I │
│   418    │ part03.html │     411 │ #  Systems of Record and Derived Data    │
└──────────┴─────────────┴─────────┴──────────────────────────────────────────┘

2 blocks with 623 tokens.
Current group id = 4
```

You can get a specific block by using the `--block_id` option:

```
$ python main.py blocks --block_id=314

                            Blocks for group id 4
┏━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ block_id ┃ tag       ┃ ~tokens ┃ block                                    ┃
┡━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│   314    │ ch03.html │     667 │ ##  Aggregation: Data Cubes and Material │
└──────────┴───────────┴─────────┴──────────────────────────────────────────┘

1 blocks with 667 tokens.
Current group id = 4
```

### Dumping blocks to a file

You can use the `dump-blocks` command to write the blocks to standard output. You can use output redirection to write the blocks to a file. For example, to write all the blocks to a file named `part03.md`, you can use the following command:

```
$ python main.py dump-blocks --tag=part03* > part03.md
```

## Prompts

Prompts are templates that are combined with the text of a block and passed off to OpenAI for completions. For example:

```
You are a technical instructional designer who ingests text content and outputs learning objectives.

Each block of text should have 1 or 2 learning objectives in the format "After reading this text, the learner will be able to..." with demonstrable verbs and completion criteria.

Each of the objectives should start with After reading this text and each learning objective should stand alone.


Here is some text in markdown format for you to use to complete the learning objectives; be sure to format them as a bullet list ("*") and not numbers:

===========================================================
{{block}}
===========================================================
```

You run the prompt against a block using the `prompt` command:

```
$ python main.py prompt --block_id=314 --prompt=prompts/learning-objective.jinja
[12:27:35] Prompting block 314 ch03.html ##  Aggregation: Data Cubes and Material                                               main.py:300
[12:27:50] Elapsed time 14.886787176132202

* After reading this text, the learner will be able to explain the concept of materialized aggregates and their role in data warehouses.
* After reading this text, the learner will be able to differentiate between a materialized view and a virtual view in a relational model.
* After reading this text, the learner will be able to describe what a data cube or OLAP cube is and how itfunctions in the context of data aggregation.
* After reading this text, the learner will be able to discuss the advantages and disadvantages of using a data cube in data warehouses.
```

You can include an optional `--msg=<message>` option to provide a message that will be stored with the prompt. This field is both useful for providing context to other users of the database, as well as being something that you can use for searching for prompts later. _NB: you must wrap the search criteria within the wildcard character \*_.

You can list the content of prompts using the `prompts` command:

```
$ python main.py prompts --tag=*part03*

* After reading this text, the learner will be able to understand the complexity of integrating multiple different data systems into one
coherent application architecture.
* After reading this text, the learner will be able to recognize the importance of implementing mechanisms for moving data from one store
to another in a large application.
```

You can search for all prompts with a message like this:

```
python main.py prompts --msg="*Generate Quiz*"
```

You can use output redirection to send the text to a file, load the file in as a new group, and then apply a new prompt to it. This enables you to chain prompts to build up more complex interactions. For example, you might have a new prompt that will summarize and condense all the individual learning objectives per section into a single learning objective for the chapter as a whole.

```
$ python main.py prompts --tag=part03* > part03-learning-objectives.md
$ python main.py load --file=part03-learning-objectives.md
$ python main.py prompt --prompt=prompts/summarize.jinja
```

### Dumping prompts to a file

You can use the `dump-prompts` command to write the prompts to standard output. You can use output redirection to write the prompts to a file. For example, to write all the prompts to a file named `part03-learning-objectives.md`, you can use the following command:

```
$ python main.py dump-prompts --tag=part03* > part03-learning-objectives.md
```

You can also include an optional `--delimiter` to specifiy how to join the prompts together. For example, if your prompts are json dictionaries, you can join them with a "," like this:

```
python main.py dump-prompts --tag="*json-topics-with-roles-no-skill*" --delimiter=",\n"
```

# Building standalone executable

First, be sure you're set up to run pyinstaller by reading [Build an executable with pyinstaller](http://www.gregreda.com/2023/05/18/notes-on-using-pyinstaller-poetry-and-pyenv/). This is another good [tutorial on pyinstaller](https://www.devdungeon.com/content/pyinstaller-tutorial).

```

pyinstaller \
 --name=promptlab \
 --add-data="/Users/odewahn/Desktop/promptlab/sql/\*:sql" \
 ../promptlab/main.py

```

# venv stuff I can never remember

```

python -m venv .venv

```

To activate:

```

source .venv/bin/activate

```

To deactivate:

```

deactivate

```

# ORM specific notes

- Spec for bulk uploaded questions -- https://github.com/oreillymedia/quiz-service/blob/9cfa6f3b85c651701c952d5ad4640ea145685a4f/docs/bulk_upload_readme.md

- List of openAI models -- https://platform.openai.com/docs/models/gpt-3-5

- Editorial test books
  ** Programming Rust
  ** Building Microservices
  \*\* Designing Machine Learning Systems

- Good chapter on splitting for LLMs -- https://learning.oreilly.com/library/view/prompt-engineering-for/9781098153427/ch03.html#id183

- List of findings from the instructional designers -- https://docs.google.com/presentation/d/1qXfZwfKPAuye778Q7ViwcS_dfe6gpDj07wFGD9dWnyo/edit#slide=id.g2aba9c57b95_0_38

-- List of sample prompts -- https://docs.google.com/document/d/14pl54fxGDEt593JFCOLPL2Ffcfuz7Al4CROll_dgGGM/edit#heading=h.k2zz50486ydb

-- Ticket with Markdown spec for question ingestion - https://github.com/oreillymedia/quiz-service/pull/136

-- Demo video - https://drive.google.com/file/d/1hEdV7E3cxOrU2Kzw9bDQYPMF1CZuyFhf/view?usp=sharing

-- text-based course brief - https://docs.google.com/document/d/1JOAj0UBv8PzE3nhNmRlOQMFsYerhQ-_hBWT_5Vn9JZw/edit

```

```
