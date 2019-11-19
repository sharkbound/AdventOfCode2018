from itertools import islice, filterfalse


def read_data():
    with open('data.txt') as f:
        return f.read()


# https://github.com/fogleman/AdventOfCode2018/blob/master/5.py
# used that repo as a reference to optimize this, tried using a deque initially, that didn't work out though
def react(data):
    res = ['']

    for c in data:
        if c == res[-1].swapcase():
            res.pop()
        else:
            res.append(c)

    # skip the empty placeholder string
    return ''.join(filter(None, res))


data = read_data()

print(
    min(
        len(react(data.replace(char.lower(), '').replace(char.upper(), '')))
        for char in set(data)
    )
)
