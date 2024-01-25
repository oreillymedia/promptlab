# Prompt Lab

- Spec for bulk uploaded questions -- https://github.com/oreillymedia/quiz-service/blob/9cfa6f3b85c651701c952d5ad4640ea145685a4f/docs/bulk_upload_readme.md

- List of openAI models -- https://platform.openai.com/docs/models/gpt-3-5

- Editorial test books
  ** Programming Rust
  ** Building Microservices
  \*\* Designing Machine Learning Systems

- Good chapter on splitting for LLMs -- https://learning.oreilly.com/library/view/prompt-engineering-for/9781098153427/ch03.html#id183

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
