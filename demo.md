# Creating a new database

```
python main.py init
```

This create a new sqlite database in the current directory that will store all the files and directories.``

# Loading in an epub file

```
python main.py load --fn=designing-data-intensive-applications.epub
```

# Review the groups and blocks

```
python main.py groups

python main.py blocks

python main.py blocks --tag=part02*

python main.py dump --block_id=19

```

# Create a new group that clean up the epub HTML

```
python main.py group --script=transformations/clean-epub.py

python main.py groups

python main.py blocks

python main.py blocks --tag=part02*

python main.py dump --block_id=39

```

HTML is more stripped down with just some of the more essential elements, like paragraphs and tags

## Changing between groups

You can see my current group is 2. If I want to go back to the old group, I can do this:

```
python main.py set-group --group_id=1

python main.py blocks
```

You can see the XML tags are back in this group. Let's set back to the most recent group.

```
python main.py set-group --group_id=2
```

## Splitting the HTML into sections

```
python main.py blocks
```

Note how big some of these blocks are -- most are over 20K tokens, which is well above the 8K token limit. So, we can do a new transformation to files into blocks that are smaller.

```
python main.py group --script=transformations/html-section-split.py

python main.py blocks
```

Now you can see we have many more blocks that are around 1000 tokens each. This is much more manageable and fits easily in the context window.

```
python main.py blocks --tag=part02*
```

# Converting HTML to Markdown

HTML is great, but LLMs do better with markdown. So, let's convert those blocks one more time.

```

python main.py group --script=transformations/html2md.py
python main.py groups
python main.py blocks --tag=part03*

```

# Creating your own transformation scripts

Let's take a quick look behind the scenes of the transformation process. Here's the script that converts the html to markdown:

```
cat transformations/html2md.py
```

It defines a main function that accepts a block of text, and then that function returns either a new single block or an array. This script gets called for every block that meets the selection criteria you define, and then writes a new block. So, if you have some kind of transformation you want to do that's special, you can just make a script that looks like this and use it yourself.

# Prompting

Now that we have our blocks that are the right size, we can start to generate some prompts. Let's start with a simple one.

```
cat prompts/learning-objective.jinja
```

This is a jinja template that will be filled in with the text from the block. Let's try it out.

```
python main.py prompt --tag=part03* --prompt=prompts/learning-objective.jinja
```

To see the results:

```
python main.py prompts --tag=part03*
```

Note that the results of each prompt are saved, so if you rerun the command on a block that has already been processed with that prompt it will skip sending it to openai and use the old version.

```
python main.py prompt --tag=part03* --prompt=prompts/learning-objective.jinja
```
