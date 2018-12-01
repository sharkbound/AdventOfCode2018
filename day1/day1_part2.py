with open('data.txt') as f:
    frequencies = [int(l) for l in f]

current = 0
seen = set()

while current not in seen:
    for freq in frequencies:
        if current in seen:
            break

        seen.add(current)
        current += freq

print(current)
