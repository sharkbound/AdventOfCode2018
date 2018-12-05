with open('data.txt') as f:
    data = f.read()


def remove_negating_units(text):
    inital_len = len(text)

    for c in set(text):
        text = text.replace(c.upper() + c.lower(), '').replace(c.lower() + c.upper(), '')

    return inital_len != len(text), text


min_len = len(data)

for char in set(data.lower()):
    datacopy = data.replace(char.lower(), '').replace(char.upper(), '')

    while True:
        changed, datacopy = remove_negating_units(datacopy)

        if not changed:
            break

    min_len = min(len(datacopy), min_len)

print(min_len)
