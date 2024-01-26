python main.py init
python main.py load
python main.py transform --script=transformations/clean_epub.py
python main.py transform --script=transformations/soup-split.py
python main.py transform --script=transformations/html2md.py
python main.py list --tag=ch05*