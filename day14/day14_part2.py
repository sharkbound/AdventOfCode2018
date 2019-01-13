from collections import deque

FILE = 'data.txt'

with open(FILE) as f:
    number = int(f.read().strip())
    target = deque(map(int, str(number)))
    scoreboard = [3, 7]

indexes = list(range(len(scoreboard)))
last_digits = deque(maxlen=len(str(number)))
searching = True

while searching:
    total = 0

    for i, v in enumerate(indexes):
        new_index = (v + scoreboard[v] + 1) % len(scoreboard)
        indexes[i] = new_index
        total += scoreboard[new_index]

    for n in map(int, str(total)):
        scoreboard.append(n)
        last_digits.append(n)

        if n == target[-1] and last_digits == target:
            searching = False
            break

print(len(scoreboard) - len(target))
