set -e
python main.py init
python main.py load --fn=data/5-paragraph-essay.txt 
python main.py transform --transformation=new-line-split
python main.py prompt --fn=data/extract-key-points.jinja
python main.py transfer-prompts --to=metadata --metadata_key=key_point