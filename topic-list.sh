# Initialize the promptlab library
python main.py init 
# Load the list topics from the file 
python main.py load --fn=cookbook/define-topics/topics.txt  
# Split the topics by newline into separate blocks
python main.py transform --transformation=new-line-split
python main.py blocks