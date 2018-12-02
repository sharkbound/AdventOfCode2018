from collections import Counter

with open('data.txt') as f:
    counts = {box_id: Counter(box_id) for box_id in map(str.rstrip, f)}

has_two_match = lambda counter: any(c == 2 for c in counter.values())
has_three_match = lambda counter: any(c == 3 for c in counter.values())

two_count = sum(1 for counter in counts.values() if has_two_match(counter))
three_count = sum(1 for counter in counts.values() if has_three_match(counter))

print(two_count * three_count)
