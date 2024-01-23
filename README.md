# Prompt Lab

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

## Useful queries

```
select operation_id, tag, position, token_count, substr(block,1,10) from blocks;
```
