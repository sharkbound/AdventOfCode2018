FILE = 'data.txt' if 1 else 'example.txt'

with open(FILE) as f:
    number = int(f.read().strip())
    scoreboard = [3, 7]

indexes = list(range(len(scoreboard)))

for _ in range(number + 10):
    total = 0
    scoreboard_length = len(scoreboard)

    if scoreboard_length >= number + 10:
        break

    for i, v in enumerate(indexes):
        new_index = (v + scoreboard[v] + 1) % scoreboard_length
        indexes[i] = new_index
        total += scoreboard[new_index]
    scoreboard.extend(map(int, str(total)))

print(''.join(map(str, scoreboard[number:number + 10])))
