
def execute(script_fn,block):
    # Create a dictionary to use as the local variables
    loc = {}
    # Read in the contents of the test.py into a string
    with open(script_fn, "r") as test_file:
        script = test_file.read()
    # Execute the code, using the block as the input
    exec(script, {"block":block}, loc)
    # Return the result
    return loc['result']


if __name__ == "__main__":
    blocks=["hello","world","this","is","a","test"]
    for block in blocks:
        result = execute("test.py",block)
        print(result)
