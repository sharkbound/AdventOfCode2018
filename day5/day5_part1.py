with open('data.txt') as f:
    data = f.read()


def remove_negating_units(text):
    inital_len = len(text)

    for c in set(text):
        text = text.replace(c.upper() + c.lower(), '').replace(c.lower() + c.upper(), '')

    return inital_len != len(text), text


while True:
    changed, data = remove_negating_units(data)

    if not changed:
        break

print(len(data))
