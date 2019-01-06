import re
from itertools import count

FILE = 'data.txt'
RE_RULE_PARSE = re.compile(r'[#.]+')


def get_alive(state):
    return {i for i, v in enumerate(state) if v == '#'}


def next_generation(state):
    new_state = set()

    for i in range(min(state) - 2, max(state) + 3):
        w = ''.join('#' if j in state else '.' for j in range(i - 2, i + 3))
        if rules[w] == '#':
            new_state.add(i)

    return new_state


with open(FILE) as f:
    state = get_alive(RE_RULE_PARSE.search(next(f)).group())
    rules = dict(map(RE_RULE_PARSE.findall, filter(None, map(str.strip, f))))

for i in count(1):
    last_state = frozenset(state)
    state = next_generation(state)

    if all(i + 1 == j for i, j in zip(last_state, state)):
        break

diff = 50000000000 - i
print(sum(i + diff for i in state))
