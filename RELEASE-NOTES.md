# v 0.1.0

## `dump` action renamed to `dump-blocks`

This was done to be more consistent with the other actions.

## You can also load transcripts of a given work:

```
python main.py load-transcript --work=9781098115302
```

## Include a `--msg` option to add a message to the prompt that you can use for later searching (as part of the tag)

```
python main.py prompt --prompt=prompts/quiz.jinja --msg="CH01 Quiz"
```

Then you can do:

```
python main.py prompts --tag="CH01 Quiz"
```

## Dump the text of prompts

```
python main.py dump-prompts --tag="CH01 Quiz" > ch01-quiz.md
```
