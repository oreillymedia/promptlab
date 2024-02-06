# Split a block into tokens of length N
def main(b):
    N = 2000
    res = []
    tokens = b.split()
    for i in range(0, len(tokens), N):
        res.append(' '.join(tokens[i:i+N]))
    return res

result =  main(block)