with open('data.txt') as f:
    frequency = sum(map(int, f))

print(frequency)
