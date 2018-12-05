import re
from collections import Counter, namedtuple
from enum import Enum
from typing import NamedTuple

GuardState = Enum('GuardState', 'ASLEEP BEGIN_SHIFT WAKES_UP')
FALLING_ASLEEP, BEGIN_SHIFT, WAKING_UP = GuardState

Log = namedtuple('Log', 'year month day hour minute text state id')
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


sleep_times = get_sleep_times()

guard_sleep_times = sorted(sleep_times.items(), key=lambda x: len(x[1]))[-1][1]
most_common_minute = max_common_count = guard_id = 0

for k, v in sleep_times.items():
    most_common = Counter(v).most_common(1)
    if most_common:
        most_common = most_common[0][0]

    count = v.count(most_common)

    if count > max_common_count:
        most_common_minute = most_common
        max_common_count = count
        guard_id = k

print('PART 2: id * minute =', guard_id * most_common_minute)
