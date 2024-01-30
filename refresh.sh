python main.py init
python main.py load --fn=designing-data-intensive-applications.epub
python main.py blocks --tag=part02*
python main.py group --script=transformations/clean-epub.py
python main.py group --script=transformations/html-section-split.py 
python main.py group --script=transformations/html2md.py
python main.py groups
python main.py blocks --tag=part03*