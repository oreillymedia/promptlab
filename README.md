# Prompt Lab

Promptlab has 3 key concepts:

- _Blocks_. Blocks of text of any length or format (text, HTML, markdown, etc). Blocks are initialized with a `load` command that reads reads files or EPUB archives.

- _Operations_. Operations are the actions that are performed on blocks. Examples include: transforming from one format to another or splitting a long block into several smaller ones. Each operation is defined by a script; some scripts are included in the repo, but users can also write their own.

- _Prompts_. Prompts are LLM results applied against a block. You define a prompt using a template defined in the `jinjia2` templating language. Promptlab combines your template with the given bloc, sends it to the LLM, and stores the result.

A few other important ideas:

- _IDs_. Each element has a unique ID. IDs are assigned automatically when the element is created. IDs are used to refer to specific blocks, operations, or prompts.

- _Tags_. Tags are used to group blocks. For example, you might want to tag all the blocks that are from a particular chapter. Tags are defined by the user.

- _Load_ -- the process of reading a file or EPUB archive and creating an initial set of blocks.

- _Init_ -- Creating a new, empty SQLITE database to store the content. By default, the database is named `promptlab.db`.

## Arguments

Arguments

- `--db` - The sqilte3 database to use. If not provided, the default is `promptlab.db`.
- `--fn`. Name of the input file. Valid extensions are `.html` and `.epub`.

## Examples

### Initialize and empty database

Creates an empty database. If no db is provided, the default is `promptlab.db`.

```
python main.py init --db=database.db
```

### Load initial text

Load an initial file. The file can be either a singel HTML file or an EPUB.

#### HTML

For HTML, the entire file is loaded and treated as block 0.

```
python main.py load --file=example.html
```

#### EPUB

In the case of an epub, all the `ITEM_DOCUMENT` files are conacatenated into a single string and treated as block 0. Each `ITEM_DOCUMENT` is placed in it's own div with an ID = to the filename, with the chapter content used as the innerHTML.

```
python main.py load --file=example.epub
```

### Transformations

python main.py transform --script=transformations/token_split.py

## Working directly with the database

https://sqlitebrowser.org/

### Useful queries

```
select operation_id, tag, position, token_count, substr(block,1,10) from blocks;
```

# ORM specific notes

- Spec for bulk uploaded questions -- https://github.com/oreillymedia/quiz-service/blob/9cfa6f3b85c651701c952d5ad4640ea145685a4f/docs/bulk_upload_readme.md

- List of openAI models -- https://platform.openai.com/docs/models/gpt-3-5

- Editorial test books
  ** Programming Rust
  ** Building Microservices
  \*\* Designing Machine Learning Systems

- Good chapter on splitting for LLMs -- https://learning.oreilly.com/library/view/prompt-engineering-for/9781098153427/ch03.html#id183
