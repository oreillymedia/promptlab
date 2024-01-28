python main.py init
python main.py load
python main.py group --script=transformations/clean_epub.py
python main.py group --script=transformations/soup-split.py 
python main.py group --script=transformations/html2md.py
python main.py groups
python main.py blocks --tag=ch05*