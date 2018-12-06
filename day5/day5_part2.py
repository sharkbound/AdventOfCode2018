with open('data.txt') as f:
    data = f.read()


def remove_negating_units(text):
    inital_len = len(text)

    for lower, upper in zip(lower_chars, upper_chars):
        text = text.replace(upper + lower, '').replace(lower + upper, '')

    return inital_len != len(text), text


min_len = len(data)
lower_chars, upper_chars = sorted(set(data.lower())), sorted(set(data.upper()))

for char in lower_chars:
    datacopy = data.replace(char, '').replace(char.upper(), '')

    while True:
        changed, datacopy = remove_negating_units(datacopy)

        if not changed:
            break

    min_len = min(len(datacopy), min_len)

print(min_len)
