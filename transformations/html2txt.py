
def main(b):
    soup = BeautifulSoup(b, 'html.parser')
    return soup.prettify()

result =  main(block)