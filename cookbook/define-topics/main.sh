# Initialize the promptlab library
promptlab init 
# Load the list topics from the file 
promptlab load --fn=topics.txt  --group_tag=topic-file
# Split the topics by newline into separate blocks
promptlab group --transformation=new-line-split
promptlab blocks