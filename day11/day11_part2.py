from itertools import count
from operator import attrgetter

import numpy as np
from collections import namedtuple

FILE = 'data.txt'

with open(FILE) as f:
    serial = int(next(f))


def power_level(x, y, serial):
    rack_id = x + 10
    return int(((rack_id * y) + serial) * rack_id / 100 % 10) - 5


Tile = namedtuple('Tile', 'x y power')
Region = namedtuple('Region', 'x y size power')

tiles = []
grid = np.zeros((300, 300), dtype=int)

for (y, x), _ in np.ndenumerate(grid):
    power = power_level(x, y, serial)
    tiles.append(Tile(x, y, power))
    grid[y, x] = power

tiles.sort(key=attrgetter('power'), reverse=True)
best_region = Region(0, 0, 0, 0)

for tile in tiles:
    last_total = -99999999
    for i in count(2):
        area = grid[tile.y:tile.y + i, tile.x:tile.x + i]
        area_sum = area.sum()

        if tile.y + i > grid.shape[0] or tile.x + i > grid.shape[1]:
            break

        if area_sum > best_region.power:
            best_region = Region(tile.x, tile.y, area.shape[0], area_sum)
            print(area_sum)

        last_total = area_sum

x, y, size, _ = best_region
print(f'{x},{y},{size}')
