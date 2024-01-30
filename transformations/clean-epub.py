

def main(b):
    # Convert the raw block of epub html to markdown
    out = md(b, heading_style="ATX")
    out = out.replace("xml version='1.0' encoding='utf-8'?", "")
    out = out.replace("\n\n", "\n")
    # Use markdown to conver the markdown to back html
    out = markdown.markdown(out)
    # Read into beautiful soup
    soup = BeautifulSoup(out, 'html.parser')
    # Prettiy print the html
    out = soup.prettify(formatter= "html")
    return out

result =  main(block)