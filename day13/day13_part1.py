from collections import defaultdict
from operator import itemgetter

import numpy as np

FILE = 'data.txt'

LEFT, RIGHT, UP, DOWN = range(4)
STRAIGHT = -1

last_turns = defaultdict(lambda: -1)

# locations are stored as (y,x)
cart_locations = {}
cart_directions = {}

# velocities are stored as (vel_y, vel_x)
direction_to_velocity = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}


def intersection_turn(cart_id):
    new_turn = (last_turns[cart_id] + 1) % 3
    last_turns[cart_id] = new_turn
    turn = (LEFT, STRAIGHT, RIGHT)[new_turn]
    direction = cart_directions[cart_id]

    if turn == STRAIGHT:
        return direction

    return {
        (UP, LEFT): LEFT,
        (UP, RIGHT): RIGHT,
        (DOWN, LEFT): RIGHT,
        (DOWN, RIGHT): LEFT,
        (LEFT, LEFT): DOWN,
        (LEFT, RIGHT): UP,
        (RIGHT, LEFT): UP,
        (RIGHT, RIGHT): DOWN,
    }[direction, turn]


def has_collision(pos):
    return tuple(cart_locations.values()).count(pos) > 1


def bumper_turn(cart_id):
    track = grid[cart_locations[cart_id]]
    direction = cart_directions[cart_id]

    if track == '\\':
        if direction == UP:
            return LEFT
        if direction == RIGHT:
            return DOWN
        if direction == LEFT:
            return UP
        return RIGHT

    if direction == UP:
        return RIGHT
    if direction == LEFT:
        return DOWN
    if direction == DOWN:
        return LEFT
    return UP


# def normalize_line()

with open(FILE) as f:
    lines = [*map(str.rstrip, f)]
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
        grid[i] = {'^': '|', 'v': '|', '<': '-', '>': '-'}[v]
        cart_id += 1

while True:
    for cart_id, pos in sorted(cart_locations.items(), key=itemgetter(1)):
        vel = direction_to_velocity[cart_directions[cart_id]]
        new_pos = pos[0] + vel[0], pos[1] + vel[1]
        cart_locations[cart_id] = new_pos
        track = grid[new_pos]
        current_direction = cart_directions[cart_id]

        if track in '\\/':
            cart_directions[cart_id] = bumper_turn(cart_id)
        elif track == '+':
            cart_directions[cart_id] = intersection_turn(cart_id)

        if has_collision(new_pos):
            y, x = new_pos
            print(f'{x},{y}')
            exit()
