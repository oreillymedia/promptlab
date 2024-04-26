import json

# This is a simple example of using lambda functions in a hash table.

FUNCTIONS = {
    "add": lambda x, y: x + y,
    "subtract": lambda x, y: x - y,
    "multiply": lambda x, y: x * y,
    "divide": lambda x, y: x / y,
}

print("add", FUNCTIONS["add"](1, 2))
print("subtract", FUNCTIONS["subtract"](1, 2))


DATA = [
    {"text": "sdf this is a long string"},
    {"text": "fgb this is a short string"},
    {"texty": "hhhhthis is a medium string"},
    {"text": "this is a very long string"},
    {"text": "this is a very very long string"},
]


TRANSFORMATIONS = {
    "text0": lambda x: x.upper(),
    "add": lambda x: x + "!",
}

# use a MAP function to apply the transformation to all the data
transformed_data = []
for d in DATA:
    row = d.copy()
    for key, transformation in TRANSFORMATIONS.items():
        if key in row.keys():
            row[key] = transformation(row[key])
    transformed_data.append(row)


print(json.dumps(transformed_data, indent=2))
