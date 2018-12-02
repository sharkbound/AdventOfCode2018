from itertools import cycle

with open('data.txt') as f:
    frequencies = [int(l) for l in f]

current = 0
seen = set()

for freq in cycle(frequencies):
    if current in seen:
        break

    seen.add(current)
    current += freq

print(current)
