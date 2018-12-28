from __future__ import annotations

from typing import List

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
        self.children: List[Node] = []
        self.metadata: List[int] = []

    def __repr__(self):
        return f'<Node children={self.children} metadata={self.metadata}>'

    def __iter__(self):
        yield self

        for child in self.children:
            yield from child


with open(FILE) as f:
    numbers = tuple(map(int, f.read().split()))
    tree = parse_tree(iter(numbers))

print(sum(sum(node.metadata) for node in tree))
