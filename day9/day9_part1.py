"""
examples:
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""

from collections import namedtuple, deque
from util import get_all_numbers


def parse_game():
    with open(FILE) as f:
        return Game(*get_all_numbers(next(f))[:2])


FILE = 'example.txt'
Game = namedtuple('Game', 'players final')
game = parse_game()


def solve():
    marbles = deque(range(game.final + 1))
    circle = [marbles.popleft()]

    while marbles:
        pass
