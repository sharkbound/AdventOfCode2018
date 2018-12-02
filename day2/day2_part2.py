from collections import Counter

has_two_match = lambda counter: any(c == 2 for c in counter.values())
has_three_match = lambda counter: any(c == 3 for c in counter.values())


def get_valid_ids():
    with open('data.txt') as f:
        for box_id in map(str.rstrip, f):
            counter = Counter(box_id)

            if has_two_match(counter) or has_three_match(counter):
                yield box_id


def diff_count(id1, id2):
    return sum(1 for c1, c2 in zip(id1, id2) if c1 != c2)


def find_valid_ids(box_ids):
    for id1 in box_ids:
        for id2 in box_ids:
            if diff_count(id1, id2) == 1:
                return id1, id2


def find_common_chars(id1, id2):
    for c1, c2 in zip(id1, id2):
        if c1 == c2:
            yield c1


ids = tuple(get_valid_ids())
id1, id2 = find_valid_ids(ids)
common = ''.join(find_common_chars(id1, id2))

print(common)
