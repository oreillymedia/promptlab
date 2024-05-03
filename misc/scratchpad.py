# Grab all H* elemenets and put them into a nested string
                for h in soup.find_all(re.compile('^h[1-4]$')):
                     print(h.name, "->", h.text)
                txt = soup.get_text()
                with open("output.txt", "w") as text_file:
                    text_file.write(txt)


if item.get_name() == 'ch03.html':
        



# Overview of the content table
def inspect_content():
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    c.execute("SELECT sort_order, fn, plain FROM content")
    for row in c:
        print(row[0],row[1],len(row[2].split(" ")))
    conn.close()


def chunks_on_headers(data, headers=['h1', 'h2']):
    soup = BeautifulSoup(data, 'html.parser')

    chunks = []
    current_chunk = []

    for tag in soup:
        print(tag.name)
        if tag.name in headers:
            if current_chunk:  # if chunk is not empty, means we can add it to chunks
                chunks.append(''.join(str(t) for t in current_chunk))
                current_chunk = []  # start a new chunk
            current_chunk.append(tag)
        else:
            current_chunk.append(tag)

    # add the final chunk that remained
    if current_chunk:
        chunks.append(''.join(str(t) for t in current_chunk))

    return chunks

def chunk_content():
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    c.execute("SELECT sort_order, fn, html FROM content where fn = 'ch03.html'")
    for row in c:
        chunks = chunks_on_headers(row[2])
        for chunk in chunks[:1]:
            #print(chunk)
            print("---------------------------------------------------")
    conn.close()

# Generate a prompt from a template and a data object
def apply_prompt(prompt, data, segment):
    with open("prompts/" + prompt + ".jinja") as f:
        template = Template(f.read())
    d = data.copy()
    d["segment"] = segment
    template = template.render(d)
    return template



if args.action == 'extract':
    extract(args.fn)
    exit(0)

if args.action == 'inspect':
    inspect_content()
    exit(0)

if args.action == 'chunk':
    chunk_content()
    exit(0)


if args.action == "read":
    if args.fn is None:
        console.log("You must provide a text file to translate")
        exit(1)
    console.log("Reading", args.fn)
    book = epub.read_epub(args.fn)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            if item.get_name() == 'ch03.html':
                html = item.get_content()
                # convert html to plain text with bs4
                soup = BeautifulSoup(html, 'html.parser')
                # Grab all H* elemenets and put them into a nested string
                for h in soup.find_all(re.compile('^h[1-4]$')):
                     print(h.name, "->", h.text)
                txt = soup.get_text()
                with open("output.txt", "w") as text_file:
                    text_file.write(txt)