
def main(b):
    soup = BeautifulSoup(b, 'html.parser')
    return soup.get_text()

result =  main(block)