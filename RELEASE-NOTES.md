# v 0.1.1

Include the segment name in the tag when pulling down a transcript. When doing this, the tag will include the segment name in the tag when pulling down a transcript. The tag now looks like this "9781098115302-001-introduction".

```
│    67    │ 9781098115302-000-introduction                                         │     224 │ # Introduction  Hi. │    68    │ 9781098115302-001-product-development-loop                             │     720 │ # Product Development │    69    │ 9781098115302-002-product-development-loop-introduction                │     721 │ ## Product
```

So, you will need to use a whildcard you're searching for all the works in a transcript.

NB: This installs a new requirement, so you will need to run:

```
pip install -r requirements.txt
```

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
