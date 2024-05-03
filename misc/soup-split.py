from bs4 import BeautifulSoup
import json

def main(b):
    # Construct a BeautifulSoup out of the raw HTML
    soup = BeautifulSoup(b, 'html.parser')
    blocks = []
    s = ""
    tag = soup.find('h1') # Find the first tag
    while tag:
        s += repr(tag).replce("\n","")
        tag = tag.nextSibling
        if tag is not None and tag.name in ["h1", "h2"]:
            blocks.append(s)
            s = ""
    return blocks


# read test.html into variable for block
with open('test2.html', 'r') as f:
    block = f.read()

result =  main(block)

# pritty print the result
for b in result:
    print("***************************************  NEW BLOCK  ***************************************")
    print(b[:40])

