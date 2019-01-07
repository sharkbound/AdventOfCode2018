from collections import defaultdict
from pprint import pprint

import numpy as np

FILE = 'example.txt'

TURN_LEFT, TURN_STRAIGHT, TURN_RIGHT = range(3)
LEFT, RIGHT, UP, DOWN = range(4)

# used for getting next turn direction at intersections
last_turns = defaultdict(lambda: -1)

cart_locations = {}
cart_directions = {}


def intersection_turn(cart_id):
    new_turn_index = (last_turns[cart_id] + 1) % 3
    last_turns[cart_id] = new_turn_index
    return (TURN_LEFT, TURN_STRAIGHT, TURN_RIGHT)[new_turn_index]


with open(FILE) as f:
    lines = [*map(str.strip, f)]
    max_len = len(max(lines, key=len))
    grid = np.array([list(line.ljust(max_len)) for line in lines])

cart_id = 0
symbol_to_direction = {'^': UP, 'v': DOWN, '<': LEFT, '>': RIGHT}
all_cart_ids = []
for i, v in np.ndenumerate(grid):
    if v in '^v<>':
        cart_locations[cart_id] = i
        cart_directions[cart_id] = symbol_to_direction[v]
        all_cart_ids.append(cart_id)
        cart_id += 1
