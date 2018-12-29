from __future__ import annotations

FILE = 'data.txt'


def parse_tree(iterator):
    node = Node(child_count=next(iterator), metadata_count=next(iterator))

    for _ in range(node.child_count):
        node.children.append(parse_tree(iterator))

    node.metadata.extend(next(iterator) for _ in range(node.metadata_count))
    return node


class Node:
    def __init__(self, child_count, metadata_count):
        self.metadata_count = metadata_count
        self.child_count = child_count
        self.children = []
        self.metadata = []

    def __str__(self):
        return f'<Node children={self.children} metadata={self.metadata}>'

    def __repr__(self):
        return f'<Node {self.child_count}c {self.metadata_count}m>'

    def __iter__(self):
        yield self

        for child in self.children:
            yield from child


def get_node_value(node):
    value = 0

    if node.children:
        for i in node.metadata:
            if i - 1 < node.child_count:
                value += get_node_value(node.children[i - 1])

        return value

    return sum(node.metadata)


with open(FILE) as f:
    numbers = tuple(map(int, f.read().split()))
    tree = parse_tree(iter(numbers))

print(get_node_value(tree))
