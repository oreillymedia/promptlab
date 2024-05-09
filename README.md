# Promptlab

Promptlab is a utility for scripting common activities when working with large amounts of text with an LLM.

```

You are a technical instructional designer who is reviewing a book about {{topic}} called {{title}}.  You're job is to create a set of learning objectives.  Here is some text in markdown format for you to use to complete the learning objectives; be sure to format them as a bullet list ("\*") and not numbers:

===========================================================
{{block}}
===========================================================

```

It has functions for:

- loading text from files or EPUBs
- transforming text using a variety of transformations
- filtering blocks
- appplying prompts to blocks
- managing metadata for prompts

Promptlab has a few key concepts:

- _Blocks_. Blocks of text of any length or format (text, HTML, markdown, etc).

- _Groups_. A group of blocks created by running a script. Examples include: transforming text from one format to another (e.g., HTML to Markdown) or splitting a long block into several smaller ones (e.g. breaking a long HTML into sections hased on heading tags like H1 or H2). Some scripts are included in the repo, but users can also write their own.

- _Prompts_. The result from a prompt template applied against a block and sent to OpenAI's LLM. Promptlab combines your template (in Jinija2 format) with the given block, sends it to the LLM, and stores the result.

- _Metadata_. Metadata is a set of key-value pairs that can be used in prompts. For example, you might have a metadata file with keys like `title`, `author`, and `topic`. You can include these keys in your prompt templates. Metadata can be included in prompts using the `--globals` option.

Promptlab uses [SQLite3](https://www.sqlite.org/index.html) as the database. The database is created automatically when you run `init`. You can use the [SQLite3 command line tool](https://www.sqlite.org/cli.html) to inspect the database directly or use a GUI like [DB Browser for SQLite](https://sqlitebrowser.org/).

# Installation

Promptlab uses Pyinstaller to create a single executable file. You can download the latest release from [PUT MORE HERE]

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
- `transfer-prompts`
- `merge-prompts-into-block`
- `version`
- `set-api-key`
- `dump`

## `init`

Creates an empty database. If no db is provided, the default is `promptlab.db`.

### Arguments

`--db` (optional) The name of the database file. Default is `promptlab.db`.

### Examples

```
promptlab init --db=database.db
```

## `load`

Loads a file or files into a new group, each of which contains a set of blocks. For example, loading an EPUB will create one new group with and optional tag you specificy, and then individual blocks for each chapter in the manifest. `load` currently supports EPUB or text (markdown, html, text, etc).

### Arguments

`--fn` (required) The name of the file to load.
`--group_tag` (optional) The tag of the group to create

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

`--where` (required) A SQL WHERE clause to filter the blocks in the current group.
`--group_tag` (optional) The tag to use for the new group.

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

`--where` (optional) A SQL WHERE clause to filter the results

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

`--where` (optional) A SQL WHERE clause to filter the results. Running `promplab blocks` will show the columns available for filtering. These are currently `['block_id', 'block_tag', 'parent_block_id', 'group_id', 'group_tag', 'block', 'token_count']`

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

`--where` (optional) A SQL WHERE clause to filter the results. Running `promplab blocks` will show the columns available for filtering. These are currently `['block_id', 'block_tag', 'parent_block_id', 'group_id', 'group_tag', 'block', 'token_count']`
`--source` (required) The source to dump. Options are `blocks` or `prompts`.
`--delimiter` (optional) The delimiter to use when joining the blocks. Default is a newline.

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

`--prompt` (required) The name of the prompt template.
`--where` (optional) A SQL WHERE clause to filter the blocks that will be used to create the prompts.
`--model` (optional) The name of the openAI model to use. Defaults to gpt-4. You can see a list of models [here]https://platform.openai.com/docs/models/overview).
`--prompt_tag` (optional) A tag to use for the prompt.
`--globals` (optional) A YAML file with global metadata values that can be used in the prompt template.
`--fake` (optional) Generates a fake response data (mostly for testing)

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

`--where` (optional) A SQL WHERE clause to filter the results. Running `promplab prompts` will show the columns available for filtering. These are currently `['prompt_id', 'block_id', 'prompt', 'response', 'model', 'prompt_tag', 'created_at']`

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

`--where` (optional) A SQL WHERE clause to filter the results. Running `promplab transfer-prompts` will show the columns available for filtering. These are currently `['prompt_id', 'block_id', 'prompt', 'response', 'model', 'prompt_tag', 'created_at']`
`--to` (required) The type of object to transfer the prompts to. Options are `blocks` or `metadata`.
`--metadata_key` (optional) The key to use for the metadata. Only valid when `--to=metadata`.

### Examples

Transfer prompts to blocks:

```
promptlab transfer-prompts --to=blocks
```

Transfer prompts to metadata:

```
promptlab transfer-prompts --to=metadata --metadata_key=key-points
```

## Metadata

### Global metadata

A file of metadata values you want to use:

```

title: Designing Data Intensive Applications
topic: data science
author: Some dude

```

These keys can then be used in a template, like this:

```

{{title}}

Has the topic {{topic}} written by {{author}}.

{{block}}

```

You include the metadata file using the `--globals` when your create your prompts:

```

promptlab prompt --fn=myprompt.jinja --globals=data.yml

```

# Development

## Building standalone executable

First, be sure you're set up to run pyinstaller by reading [Build an executable with pyinstaller](http://www.gregreda.com/2023/05/18/notes-on-using-pyinstaller-poetry-and-pyenv/). This is another good [tutorial on pyinstaller](https://www.devdungeon.com/content/pyinstaller-tutorial).

From the root directory, run the following command:

```

pyinstaller -F \
 --name=promptlab \
 --add-data="sql:sql" \
 main.py

```

# venv

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
