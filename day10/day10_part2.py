import re
from itertools import count
from operator import itemgetter
from typing import NamedTuple

FILE = 'data.txt'


class Marker(NamedTuple):
    x: int
    y: int
    vx: int
    vy: int

    def move(self):
        return Marker(self.x + self.vx, self.y + self.vy, self.vx, self.vy)


def sorter_func(m):
    return abs(m.x) + abs(m.y)


def min_at(i, items):
    return min(map(itemgetter(i), items))


def max_at(i, items):
    return max(map(itemgetter(i), items))


def get_bounds(markers):
    x0, y0 = min_at(0, markers), min_at(1, markers)
    x1, y1 = max_at(0, markers), max_at(1, markers)

    return x0, y0, x1, y1


def get_area(markers):
    x0, y0, x1, y1 = get_bounds(markers)

    return abs(x1 - x0) * abs(y0 - y1)


def advance_state(markers):
    return tuple(m.move() for m in markers)


with open(FILE) as f:
    markers = tuple(Marker(*map(int, re.findall(r'-?\d+', line))) for line in f)

last_area, last_state = get_area(markers), markers

for i in count():
    new_state = advance_state(last_state)
    area = get_area(new_state)

    if area > last_area:
        break

    last_area = area
    last_state = new_state

print(i)
