#
# Split an HTML into blocks based on the h1 and h2 tags
#
def main(b):
    # Construct a BeautifulSoup out of the raw HTML
    soup = BeautifulSoup(b, 'html.parser')
    blocks = []
    s = ""
    tag = soup.find('h1') # Find the first tag
    while tag:
        s += repr(tag).replace("\n","")
        tag = tag.nextSibling
        if tag is not None and tag.name in ["h1", "h2"]:
            blocks.append(s.replace("'\n'","\n"))
            s = ""
    return blocks

result =  main(block)
