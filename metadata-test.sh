set -e
python main.py init
python main.py load --fn=data/5-paragraph-essay.txt 
python main.py transform --transformation="new-line-split,  sentence-split"
python main.py filter --where="token_count > 1" --group_tag="paragraphs"
python main.py prompt --fn=data/extract-key-points.jinja --model=gpt-3.5-turbo --prompt_tag="extract-key-points"
python main.py merge-prompts-into-block --group_tag="paragraph-summary"
python main.py prompt --fn=data/summarize-key-points.jinja --prompt_tag="summarize-key-points"
python main.py dump-prompts --where="prompt_tag like 'summarize%'" --delimiter=" "