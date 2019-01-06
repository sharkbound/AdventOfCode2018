"""
the next_generation() function was borrowed from here:
https://www.michaelfogleman.com/aoc18/#12

this one gave me a lot of trouble the way i was trying to do it
so i just grabbed a working solution i found with some of my own ways of doing it
"""

import re

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

for _ in range(20):
    state = next_generation(state)

print(sum(state))
