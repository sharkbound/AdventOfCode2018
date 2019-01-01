"""
examples:
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""

from collections import namedtuple, deque, defaultdict
from util import get_all_numbers

FILE = 'data.txt'
Game = namedtuple('Game', 'players final')

with open(FILE) as f:
    game = Game(*get_all_numbers(next(f))[:2])


def rotate_index(i, size):
    if i > size:
        i -= size
    elif i < 0:
        i += size
    return i


def solve():
    final = game.final * 100 + 1
    marbles = deque(range(final))
    circle = [marbles.popleft()]
    scores = defaultdict(int)
    index = 0
    player = 1
    counter = 1

    while marbles:
        next_marble = marbles.popleft()

        if counter != 23:
            index = rotate_index(index + 2, len(circle))
            circle.insert(index, next_marble)

        else:
            removed_index = rotate_index(index - 7, len(circle))
            removed = circle[removed_index]
            index = removed_index
            del circle[index]
            scores[player] += next_marble + removed

        player = max((player + 1) % (game.players + 1), 1)

        if counter >= 23:
            counter = 0
        counter += 1

    print(max(scores.values()))


print(solve(game.players, game.final + 1))
print(solve(game.players, game.final * 100 + 1))

# solve()
