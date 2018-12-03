"""
Each claim's rectangle is defined as follows:
The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
"""

import re
from collections import namedtuple
import numpy as np

Claim = namedtuple('Claim', 'id left_edge_inches top_edge_inches width height')
Box = namedtuple('Box', 'x1 y1 x2 y2')

re_info = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


def parse_lines():
    with open('data.txt') as f:
        for line in f:
            yield Claim(*map(int, re_info.findall(line)[0]))


def claim_to_indexes(c: Claim):
    return (
        slice(c.top_edge_inches, c.top_edge_inches + c.height),
        slice(c.left_edge_inches, c.left_edge_inches + c.width)
    )


claims = tuple(parse_lines())
grid = np.zeros((1000, 1000))

for c in claims:
    grid[claim_to_indexes(c)] += 1

for c in claims:
    if grid[claim_to_indexes(c)].sum() == c.width * c.height:
        print(c.id)
        break
