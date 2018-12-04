import re
from collections import namedtuple
from enum import Enum
from typing import NamedTuple

GuardState = Enum('GuardState', 'ASLEEP BEGIN_SHIFT WAKES_UP')
ASLEEP, BEGIN_SHIFT, WAKES_UP = GuardState


# [1518-07-18 23:57] Guard #157 begins shift
# using typing.NamedTuple since i can override __repr__ with it
class Log(NamedTuple):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    text: str
    state: GuardState
    id: int

    # overriding __repr__ to assist is reading the testing output
    def __repr__(self):
        return f'[{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}] {self.text}'


# Log = namedtuple('Log', 'year month day hour minute text state id')
re_log = re.compile(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)] (.+)')
FILE = 'data.txt'


def parse(line):
    year, month, day, hour, minute, text = re_log.search(line).groups()

    m = re.search(r'Guard #(\d+)', text)
    if m:
        guard_id = int(m[1])
    else:
        guard_id = None

    if text.endswith('begins shift'):
        state = BEGIN_SHIFT
    elif text.endswith('falls asleep'):
        state = ASLEEP
    elif text.endswith('wakes up'):
        state = WAKES_UP
    else:
        raise ValueError('could not get guard state from log message')

    return Log(year, month, day, hour, minute, text, state, guard_id)


with open(FILE) as f:
    logs = sorted(map(parse, f), key=lambda log: (log.year, log.month, log.day, log.hour, log.minute))
