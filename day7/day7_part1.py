from dataclasses import dataclass, field
from operator import itemgetter
from typing import List, Set

import re


@dataclass
class Step:
    id: str
    requirements: Set[str] = field(default_factory=set, compare=False)

    def all_requirements_done(self, steps_done):
        return all(r in steps_done for r in self.requirements)


def parse_lines():
    ret = {}

    with open('data.txt') as f:
        for line in f:
            requirement_id, step_id = re.findall(r'\b\w\b', line)

            if requirement_id not in ret:
                ret[requirement_id] = Step(requirement_id)

            if step_id not in ret:
                ret[step_id] = Step(step_id)

            ret[step_id].requirements.add(requirement_id)

    return ret


def solve():
    steps_done = set()
    steps_sorted = sorted(steps.items(), key=itemgetter(0))
    order = []

    while len(order) != len(steps_sorted):
        for id, step in steps_sorted:
            if id not in steps_done and step.all_requirements_done(steps_done):
                steps_done.add(id)
                order.append(id)
                break

    return order


steps = parse_lines()
print(''.join(solve()))
