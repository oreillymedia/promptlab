set -e
python main.py init
python main.py load --fn=designing-data-intensive-applications.epub
python main.py filter --where="block_tag like 'ch%'"
python main.py transform --transformation=clean-epub
python main.py transform --transformation=html-h1-split
python main.py transform --transformation=html2md  
python main.py filter --where="token_count > 1000" --group_tag=key-sections
python main.py prompt --fn=prompts/learning-objective.jinja --fake
python main.py blocks