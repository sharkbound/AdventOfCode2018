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

tiles = []
grid = np.zeros((300, 300), dtype=int)

for (y, x), _ in np.ndenumerate(grid):
    power = power_level(x, y, serial)
    tiles.append(Tile(x, y, power))
    grid[y, x] = power

tiles.sort(key=attrgetter('power'), reverse=True)
best_tile = Tile(0, 0, -1)
best_total = 0

for tile in tiles:
    if tile.power <= 1:
        break

    surrounding_sum = grid[tile.y - 1:tile.y + 2, tile.x - 1:tile.x + 2].sum()
    if surrounding_sum > best_total:
        best_total = surrounding_sum
        best_tile = tile

print(f'{best_tile.x - 1},{best_tile.y - 1}')
