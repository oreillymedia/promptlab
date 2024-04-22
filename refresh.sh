python main.py init
python main.py load --fn=designing-data-intensive-applications.epub
python main.py blocks --tag=part02*
python main.py group --transformation=clean-epub
python main.py group --transformation=html-section-split
python main.py group --transformation=html2md
python main.py groups
python main.py blocks --tag=part03*