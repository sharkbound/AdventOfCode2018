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

    @property
    def as_tuple(self):
        return tuple(self.registers)

    def __eq__(self, other):
        return list(other) == self.as_list

    def __repr__(self):
        return repr(self.as_list)


@dataclass
class Instruction:
    id: int
    a: int
    b: int
    c: int

    def __iter__(self):
        yield from (self.id, self.a, self.b, self.c)

    @property
    def input(self):
        return self.a, self.b

    @property
    def output(self):
        return self.c


(
    REG_A,
    REG_B,
    REG_C,
    REG_D
) = range(4)

(
    ADDI,
    SETI,
    MULR
) = range(3)

RE_LINE_INSTRUCTION = re.compile('(\d) (\d) (\d) (\d)')
RE_SAMPLE_INSTRUCTION = re.compile(r'\[(\d), (\d), (\d), (\d)\]')


def parse_line_instruction(line):
    if match := RE_LINE_INSTRUCTION.match(line):
        return Instruction(*map(int, match.groups()))


def parse_sample_instruction(line):
    if match := RE_SAMPLE_INSTRUCTION.search(line):
        return Instruction(*map(int, match.groups()))


# noinspection PyUnboundLocalVariable
def solve_part_1():
    possiblies = defaultdict(set)
    memory = Memory()
    before = after = False

    for line in read_lines():
        is_after = 'After' in line
        is_before = 'Before' in line
        is_sample = is_before or is_after

        if is_after:
            after = True
            before = False
        elif is_before:
            before = True
            after = False
        elif after and line.replace(' ', '').isnumeric():
            before = False
            after = False

        if is_before or is_after:
            instruction = parse_sample_instruction(line)
        else:
            instruction = parse_line_instruction(line)

        if is_before:
            memory.override(*instruction)
        elif is_after:
            expected = tuple(map(int, RE_SAMPLE_INSTRUCTION.search(line).groups()))
            assert memory.as_tuple == expected, f'\nexpected memory to be {expected}\nit was actually {memory.as_tuple}\nthe line was {line!r}'
        elif is_sample:
            pass

    # if match := RE_INSTRUCTION.match(line):
    #     instruction = Instruction(*map(int, match.groups()))
    #     print(instruction)


print(solve_part_1())
