def solve(ids):
    for id1 in ids:
        for id2 in ids:
            if sum(1 for c1, c2 in zip(id1, id2) if c1 != c2) == 1:
                yield from (c1 for c1, c2 in zip(id1, id2) if c1 == c2)
                return


print(*solve([*map(str.rstrip, open('data.txt'))]), sep='')
