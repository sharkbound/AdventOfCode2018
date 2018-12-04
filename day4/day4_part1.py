import re
from collections import Counter
from enum import Enum
from typing import NamedTuple

GuardState = Enum('GuardState', 'ASLEEP BEGIN_SHIFT WAKES_UP')
FALLING_ASLEEP, BEGIN_SHIFT, WAKING_UP = GuardState


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
re_log = re.compile(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)')
FILE = 'data.txt'


def parse(line):
    *args, text = re_log.search(line).groups()
    year, month, day, hour, minute = map(int, args)
    state = guard_id = None

    m = re.search(r'Guard #(\d+)', text)
    if m:
        guard_id = int(m[1])

    if text.endswith('begins shift'):
        state = BEGIN_SHIFT

    elif text.endswith('falls asleep'):
        state = FALLING_ASLEEP

    elif text.endswith('wakes up'):
        state = WAKING_UP

    return Log(year, month, day, hour, minute, text, state, guard_id)


with open(FILE) as f:
    logs = sorted(map(parse, f), key=lambda log: (log.year, log.month, log.day, log.hour, log.minute))
    all_guard_ids = [l.id for l in logs if l.state is BEGIN_SHIFT]


def get_sleep_times():
    sleep_times = {id: [] for id in all_guard_ids}
    sleep_start = -1
    guard_id = -1

    for l in logs:
        if l.state is BEGIN_SHIFT:
            guard_id = l.id

        elif l.state is FALLING_ASLEEP:
            sleep_start = l.minute

        elif l.state is WAKING_UP:
            sleep_times[guard_id].extend(range(sleep_start, l.minute))
            sleep_start = -1

    return sleep_times


times = get_sleep_times()

sleepiest_guard_id, guard_sleep_times = sorted(times.items(), key=lambda x: len(x[1]))[-1]
sleepiest_minute = Counter(guard_sleep_times).most_common(1)[0][0]

print('PART 1: id * minute =', sleepiest_guard_id * sleepiest_minute)
