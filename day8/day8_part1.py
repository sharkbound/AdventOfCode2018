FILE = 'data.txt'


def parse_lines():
    with open(FILE) as f:
        return list(map(int, f.read().split()))


class Tree:
    def __init__(self, value=None):
        self.left = None
        self.right = None
        self.value = value


print(parse_lines())
