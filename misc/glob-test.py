import glob


def find_files(fname):
    return glob.glob(fname)


print(find_files("*.py"))
