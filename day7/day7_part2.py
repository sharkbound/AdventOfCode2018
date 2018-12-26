import re
from dataclasses import dataclass, field
from operator import itemgetter
from typing import Set
from string import ascii_uppercase

FILE = 'data.txt'
DELAY = 61
MAX_JOBS = 5


class AssemblyJobPool:
    def __init__(self):
        self.maxjobs = MAX_JOBS
        self.runtime_ticks = 0
        self.jobs = {}

    @property
    def has_free_job(self):
        return len(self.jobs) < self.maxjobs

    @property
    def empty(self):
        return not self.jobs

    def add_job(self, data, ticks_to_complete):
        if not self.has_free_job:
            return

        self.jobs[data] = [data, ticks_to_complete, 0]

    def tick(self, step=1):
        self.runtime_ticks += step
        for job in self.jobs.values():
            job[-1] += step

    def remove_completed_jobs(self):
        for j in [j for j, complete_ticks, active_ticks in self.jobs.values() if active_ticks >= complete_ticks]:
            del self.jobs[j]
            yield j

    def __str__(self):
        return ', '.join(
            f'JOB{{{data} %{min(100, (active_ticks / complete_ticks) * 100):.0f} {active_ticks}/{complete_ticks}}}' for
            data, complete_ticks, active_ticks in self.jobs.values())

    def __len__(self):
        return len(self.jobs)

    def __contains__(self, item):
        return item in self.jobs


@dataclass
class Step:
    id: str
    requirements: Set[str] = field(default_factory=set, compare=False)

    def all_requirements_done(self, steps_done):
        return all(r in steps_done for r in self.requirements)

    @property
    def time_to_complete(self):
        return 61 + ascii_uppercase.index(self.id)


def parse_lines():
    ret = {}

    with open(FILE) as f:
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
    pool = AssemblyJobPool()

    while True:
        steps_done.update(pool.remove_completed_jobs())

        for id, step in steps_sorted:
            if id in steps_done or id in pool:
                continue

            if step.all_requirements_done(steps_done):
                pool.add_job(id, DELAY + ascii_uppercase.index(id))

        if pool.empty:
            return pool.runtime_ticks

        pool.tick()


steps = parse_lines()
print(solve())
