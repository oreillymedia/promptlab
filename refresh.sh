python main.py init
python main.py load
python main.py group --script=transformations/clean-epub.py
python main.py group --script=transformations/html-section-split.py 
python main.py group --script=transformations/html2md.py
python main.py groups
python main.py blocks --tag=ch05*