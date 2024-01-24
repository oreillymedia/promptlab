

def main(b):

    # https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches

    # Find all the <h1> tags
    h1s = list(find_all(b, "<h1"))
    h2s = list(find_all(b, "<h2"))
    # merge the lists
    h1s.extend(h2s)
    # Sort the list
    h1s.sort()
    # Split the html into blocks
    blocks = []
    for i in range(len(h1s)):
        if i == len(h1s) - 1:
            blocks.append(b[h1s[i]:])
        else:
            blocks.append(b[h1s[i]:h1s[i+1]])
    return blocks

result =  main(block)