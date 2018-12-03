"""
Each claim's rectangle is defined as follows:
The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
"""

import re
from collections import namedtuple

Claim = namedtuple('Claim', 'id left_edge_inches top_edge_inches width height')
Box = namedtuple('Box', 'x1 y1 x2 y2')

# #1 @ 45,64: 22x22
re_info = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


def parse_lines():
    with open('data.txt') as f:
        for line in f:
            yield Claim(*map(int, re_info.findall(line)[0]))


def box_coords(c: Claim):
    return Box(
        x1=c.left_edge_inches,
        y1=c.top_edge_inches,
        x2=c.left_edge_inches + c.width,
        y2=c.top_edge_inches + c.height
    )


def point_in_box(box: Box, x, y):
    return box.x1 <= x >= box.x2 and box.y1 <= y >= box.y2


def collides(box1: Box, box2: Box):
    return (
            point_in_box(box1, box2.x1, box2.y1)
            or point_in_box(box1, box2.x2, box2.y2)
            or point_in_box(box2, box1.x1, box1.y1)
            or point_in_box(box2, box1.x2, box1.y2)
    )


def get_overlap(box1: Box, box2: Box):
    # if point_in_box(box1, box2.x1, box2.y1):
    #     x1, y1 = box2.x1, box2.y1
    # elif point_in_box(box2, box1.x1, box1.y1):
    #     x1, y1 = box1.x1, box1.y1
    # else:
    #     raise ValueError('cannot find x1, y1')
    #
    # if point_in_box(box1, box2.x2, box2.y2):
    #     x2, y2 = box2.x2, box2.y2
    # elif point_in_box(box2, box1.x2, box1.y2):
    #     x2, y2 = box1.x2, box1.y2
    # else:
    #     raise ValueError('cannot find x2, y2')

    x1, y1 = max(box1.x1, box2.x1), max(box1.y1, box2.y1)
    x2, y2 = min(box1.x2, box2.x2), min(box1.y2, box2.y2)

    return (x2 - x1) * (y2 - y1)


claims = tuple(parse_lines())


def main():
    counted = set()
    overlap = 0

    for c1 in claims:
        for c2 in claims:
            if c1.id == c2.id:
                continue

            box1 = box_coords(c1)
            box2 = box_coords(c2)
            pair = box1, box2

            if collides(box1, box2) and pair not in counted:
                overlap += get_overlap(box1, box2)
                counted.add(pair)

    # this code does not work
    print(overlap)


main()
