import re
from collections import defaultdict
from dataclasses import dataclass
from typing import NamedTuple

from read import read_lines


class Memory:
    def __init__(self):
        self.registers = [0] * 4

    def __getitem__(self, item):
        return self.registers[item]

    def __setitem__(self, key, value):
        self.registers[key] = value

    def override(self, a, b, c, d):
        self[:] = a, b, c, d

    @property
    def as_list(self):
        return self.registers.copy()

    def __eq__(self, other):
        return list(other) == self.as_list

    def __repr__(self):
        return repr(self.as_list)


@dataclass
class Instruction:
    id: str
    a: int
    b: int
    c: int

    @property
    def is_instruction(self):
        return self.id.isnumeric()

    @property
    def instruction(self):
        return int(self.id)

    @property
    def input(self):
        return self.a, self.b

    @property
    def output(self):
        return self.c


REG_A = 0
REG_B = 1
REG_C = 2
REG_D = 3

ADDI = 1
SETI = 2
MULI = 3


def solve_part_1():
    possiblies = defaultdict(set)
    memory = Memory()
    before = after = False

    for line in read_lines():
        if 'After' in line:
            after = True
            before = False
        elif 'Before' in line:
            before = True
            after = False
        elif after and line.replace(' ', '').isnumeric():
            before = False
            after = False

        if before or after:
            print(before, after, line)


print(solve_part_1())
