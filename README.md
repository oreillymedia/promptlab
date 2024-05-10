# Promptlab

Promptlab is a utility for managing common activities when processing large amounts of text with an LLM. It lets you:

- Load text from files or EPUBs into a database
- Transform text using a variety of transformations. For example, convert an EPUB to markdown, split a long block into smaller blocks, or split a block into sentences. A lot of this work is required to fit the text into the LLM's token limit.
- Filter out blocks of text. For example, you might only want to process one chapter in a book.
- Apply templated prompts to your blocks and send them to an LLM. You can use metadata in your prompts to make them more dynamic. For example, you might have a metadata file with keys like `title`, `author`, and `topic`. You can include these keys in your prompt templates.

Propmptlab helps you massage text into smaller blocks that can be fed into an LLM using a [Jinja](https://jinja.palletsprojects.com/) template. This template contains the text of your prompt, along with variables that get passed in from the block. For example, you might have a template like this with three variables -- a topic, a title, an author, and a block of text:

```
You are a technical instructional designer who is reviewing
a book about {{topic}} called {{title}} by {{author}}.  Your job is to
summarize the key points in each section.  Here is some text in
markdown format for you to use summarize:

{{block}}
```

You supply the metadata in a YAML file, like this:

```yml
title: Fooing the Bar
topic: Python Programming
author: A. N. Other
```

When you run the `prompt` command in Promptlab, a block of text and the metadata is passed into the template:

```jinja
You are a technical instructional designer who is reviewing
a book about Python Programming called Fooing the Bar by A. N. Other.
Your job is to summarize the key points in each section.  Here is
some text in markdown format for you to use summarize:

<BLOCK OF TEXT>
```

This fully rendered text is sent to an LLM for completion. The process is repeated for the other blocks of content until all the sections you select are processed. You can then convert these resposes into new blocks or metadata, or just dump them out an save them in a file.

Finally, Promptlab can be used as part of a script to automate the process of generating prompts and responses. For example, here's an example of how tou might summarize the full contents of a book:

```bash
# Make sure the bash script exits if any command fails
set -e
# Create a new database
promptlab init
# Load the epub
promptlab load --fn=book.epub
# Apply a filter to only work on chapter
promptlab filter --where="block_tag like 'ch%'"
# Clean up the extraneous HTML, split the text into sections, and convert to markdown
promptlab transform --transformation="clean-epub, html-h1-split, html2md"
# Only work on sections with more than 1000 tokens
promptlab filter --where="token_count > 1000" --group_tag=key-sections
# Apply the summarization template using the metadata in metadata.yml
promptlab prompt --fn=summarize.jinja --globals=metadata.yml
# Write the results to a file
promptlab dump --source=prompts > key-points.md
```

# Installation

Promptlab uses Pyinstaller to create a single executable file. To install it, [download the latest release](https://github.com/oreillymedia/promptlab/releases) and put it somewhere in your path. To test that it's working correctly, run:

```
promptlab version
```

Note that it's pretty slow to start. This is an artifact of the way Pyinstaller works when it builds a single file for distribution. Once it's running, it's pretty fast. I should probably make a REPL for it.

# Usage

- Create a directory to hold your content. For example, you might download an EPUB or some files there.
- Run `promptlab init` to create a new database. This will create a SQLITE database called `promptlab.db` in the current directory (unless you override the name with the `--db` option).
- Load the content into the database with `promptlab load --fn=*.epub`. This will create a new group with blocks for each chapter in the EPUB.

At this point, you might need to poke around a bit in the data to figure out how it's structured. You can use the `dump` command to inspect the blocks. Once you have an idea of how it looks, you can use the various transformations to clean up the data and split it into smaller blocks that will fit into the LLM's context window, which is typically around 8192 tokens. For example, you might use the `html-h1-split` transformation to split the text into blocks based on the H1 tags in the HTML.

Finally, you might also want to restrict the blocks you're working with to a subset of the data. You can use the `filter` command to do this. For example, you might only want to work with blocks that have more than 1000 tokens.

Next, you can start creating prompt templates. These should be Jinja templates that include the text of the prompt and any metadata you want to include. When you run the `prompt` command, you'll pass in the name of the template and the metadata file, and each block in the set you supply will be passed into the template in the `{{block}}` variable. The fully rendered prompt will be sent to the LLM for completion.

Finally, you can use the `dump` command to write the results to a file, or transfer them into other blocks or metadata.

Once you've found the right set of transformations and filters, you can script the whole process to automate the generation of prompts and responses and save it as a bash script.

# Command Reference

Promptlab has the following commands:

- `init` -- create a new sqlite database to store data
- `load` -- load a file or files into a new group with blocks
- `transform` -- create a new group of blocks by applying a transformation to the current group
- `filter` -- create a new group of blocks by applying a filter to the current group
- `blocks` -- list all blocks in the current group
- `groups` -- list all groups
- `set-group` -- set the current group
- `prompt` -- generate prompts from a set of blocks based on metadata and a template
- `prompts` -- list all prompts
- `transfer-prompts` -- convert prompts into blocks or metadata
- `version` - show the version of the software
- `set-api-key` - set the api key used for the LLM
- `dump` - write blocks or prompts to standard output

## `init`

Creates an empty database. If no db is provided, the default is `promptlab.db`.

### Arguments

- `--db` (optional) The name of the database file. Default is `promptlab.db`.

### Examples

```
promptlab init --db=database.db
```

## `load`

Loads a file or files into a new group, each of which contains a set of blocks. For example, loading an EPUB will create one new group with and optional tag you specificy, and then individual blocks for each chapter in the manifest. `load` currently supports EPUB or text (markdown, html, text, etc).

### Arguments

- `--fn` (required) The name of the file to load.
- `--group_tag` (optional) The tag of the group to create

### Examples

Load all HTML files:

```
promptlab load --fn=*.html
```

Loading an EPUB will create a group for each chapter and a block for each chapter:

```
promptlab load --fn=example.epub
```

You can provide a tag for the group so you can reference it later, like this:

```
promptlab load --fn=example.epub --group_tag=example
```

## `transform`

The `transform` command creates new groups of blocks by applying a transformation rule to the current group. The transformations are:

- `token-split` - Breaks text into chunks of 2000 tokens
- `clean-epub` - Simplifies the HTML of an EPUB
- `html-h1-split` - Breaks HTML into blocks based on H1 tags
- `html-h2-split` - Breaks HTML into blocks based on H2 tags
- `html2md` - Converts HTML to Markdown
- `html2txt` - Converts HTML to text
- `new-line-split` - Splits text into blocks based on new lines
- `sentence-split` - Splits text into blocks based on sentences

### Arguments

`--transformation` (required) The name of the transformation to run; you can run multiple transformations by providing a comma-separated list of transformations.
`--group_tag` (optional) The tag to use for the new group. (Only valid when there are is a single transformation.)

### Examples

Apply 3 transformations to the current group:

```
promptlab transform --transformation="clean-epub, html-h1-split, html2md"
```

Name a group:

```
promptlab transform --transformation="clean-epub" --group_tag=cleaned-up-files
```

## `filter`

The `filter` command creates a new group of blocks by applying a filter to the current group. The filter is a SQL WHERE clause that filters the blocks in the current group. The filtered group is then set to the current group.

### Arguments

- `--where` (required) A SQL WHERE clause to filter the blocks in the current group.
- `--group_tag` (optional) The tag to use for the new group.

### Examples

Filter blocks whose tag name starts with "chapter":

```
promptlab filter --where="block_tag like 'chapter%'"
```

Filter blocks with more than 1000 tokens:

```
promptlab filter --where="token_count > 1000"
```

## `groups`

Lists all groups.

### Arguments

- `--where` (optional) A SQL WHERE clause to filter the results

### Examples

Show all current groups:

```
promptlab groups
```

Show all groups with more than 50 blocks:

```
promptlab groups --where="block_count > 50"
```

## `set-group`

Sets the group to the provided group tag.

### Arguments

`--group_tag` (required) The group tag to set as the current group.

### Examples

```
promptlab set-group --group_tag=example
```

## `blocks`

List all blocks in the current group:

### Arguments

- `--where` (optional) A SQL WHERE clause to filter the results. Running `promplab blocks` will show the columns available for filtering. These are currently `['block_id', 'block_tag', 'parent_block_id', 'group_id', 'group_tag', 'block', 'token_count']`

### Examples

Show all blocks in the current group

```
promptlab blocks
```

Show all blocks with more than 1000 characters:

```
promptlab blocks --where="token_count > 1000"
```

Select all blocks that match a tag:

```
promptlab blocks --where="block_tag like 'chapter%'"
```

## `dump`

Write blocks or prompts to standard output.

### Arguments

- `--source` (required) The source to dump. Options are `blocks` or `prompts`.
- `--where` (optional) A SQL WHERE clause to filter the results. Running `promplab blocks` will show the columns available for filtering. These are currently `['block_id', 'block_tag', 'parent_block_id', 'group_id', 'group_tag', 'block', 'token_count']`
- `--delimiter` (optional) The delimiter to use when joining the blocks. Default is a newline.

### Examples

Dump all blocks to standard output:

```
promptlab dump
```

Dump all blocks with more than 1000 characters:

```
dump --source=blocks --where="block_tag like 'part03%'"
```

Dump all blocks with a comma delimiter:

```
promptlab dump --source=blocks --delimiter=","
```

## `prompt`

Generate prompts from a set of blocks based on metadata and a template, and then used an LLM complection endpoint to generate completions.

### Arguments

- `--prompt` (required) The name of the prompt template.
- `--where` (optional) A SQL WHERE clause to filter the blocks that will be used to create the prompts.
- `--model` (optional) The name of the openAI model to use. Defaults to gpt-4. You can see a list of models [here](https://platform.openai.com/docs/models/overview).
- `--prompt_tag` (optional) A tag to use for the prompt.
- `--globals` (optional) A YAML file with global metadata values that can be used in the prompt template.
- `--fake` (optional) Generates a fake response data (mostly for testing)

### Examples

You run the prompt against a block using the `prompt` command:

```
promptlab prompt --fn=extract-key-points.jinja --model=gpt-3.5-turbo --prompt_tag="extract-key-points"
```

Prompt for a specific group:

```
promptlab prompt --fn=summarize.jinja --where="block_tag like 'ch12%'"
```

Prompt and provide global metadata from a file:

```
promptlab prompt --fn=extract-key-points.jinja --globals=metadata.yml
```

## `prompts`

Prints all prompts to standard output.

### Arguments

- `--where` (optional) A SQL WHERE clause to filter the results. Running `promplab prompts` will show the columns available for filtering. These are currently `['prompt_id', 'block_id', 'prompt', 'response', 'model', 'prompt_tag', 'created_at']`

### Examples

Print all prompts:

```
promptlab prompts
```

Print all prompts with a specific tag:

```
promptlab prompts --where="prompt_tag like 'ch12%'"
```

## `transfer-prompts`

Convert prompts into blocks or metadata. This is useful is you want to do later processing with a prompt.

### Arguments

- `--where` (optional) A SQL WHERE clause to filter the results. Running `promplab transfer-prompts` will show the columns available for filtering. These are currently `['prompt_id', 'block_id', 'prompt', 'response', 'model', 'prompt_tag', 'created_at']`
- `--to` (required) The type of object to transfer the prompts to. Options are `blocks` or `metadata`.
- `--metadata_key` (optional) The key to use for the metadata. Only valid when `--to=metadata`.

### Examples

Transfer prompts to blocks:

```
promptlab transfer-prompts --to=blocks
```

Transfer prompts to metadata:

```
promptlab transfer-prompts --to=metadata --metadata_key=key-points
```

## `version`

Prints the version of the software.

### Examples

```
promptlab version
```

## `set-api-key`

Sets the API key used for the LLM. This is required to use the `prompt` command. NB: This key is stored in plain text in a file called `~/.promptlab`.

### Examples

```
promptlab set-api-key
```

# Development

This section is a little light right now since this is a single person project. I should probably write some tests, for example....

## Set up the environment

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

## Install the requirements

```
pip install -r requirements.txt
```

I've noticed that sometimes `pyinstaller` doesn't pick up these packages unless you also run them in the global environment where Python is installed, rather than in the virtual environment. I'm not sure why this is, but it's something to keep in mind.

## Building standalone executable

First, be sure you're set up to run pyinstaller by reading [Build an executable with pyinstaller](http://www.gregreda.com/2023/05/18/notes-on-using-pyinstaller-poetry-and-pyenv/). This is another good [tutorial on pyinstaller](https://www.devdungeon.com/content/pyinstaller-tutorial). It took a bit of finagling to make this work, so YMMV.

From the root directory, run the following command:

```

pyinstaller -F \
 --name=promptlab \
 --add-data="sql:sql" \
 main.py

```
