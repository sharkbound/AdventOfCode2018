import re
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from pprint import pprint
from typing import NamedTuple, DefaultDict, Set

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

    @contextmanager
    def temp(self, setup: tuple):
        prev_state = self.as_tuple
        self.override(*setup)
        yield
        self.override(*prev_state)

    @property
    def as_list(self):
        return self.registers.copy()

    @property
    def as_tuple(self):
        return tuple(self.registers)

    def __eq__(self, other):
        return list(other) == self.registers

    def __repr__(self):
        return f'<Memory {self.registers!r}>'


@dataclass
class Instruction:
    op: int
    a: int
    b: int
    c: int

    def __iter__(self):
        yield from (self.op, self.a, self.b, self.c)

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

RE_INSTRUCTION = re.compile('(\d+),? (\d+),? (\d+),? (\d+)')


def find_instruction(line):
    if match := RE_INSTRUCTION.search(line):
        return Instruction(*map(int, match.groups()))


def extract_numbers(line):
    return tuple(map(int, RE_INSTRUCTION.search(line).groups()))


operations = []


def register(id, func):
    operations.append((id, func))
    return id, func


ADDR, addr = register('ADDR', lambda mem, i: mem[i.a] + mem[i.b])
ADDI, addi = register('ADDI', lambda mem, i: mem[i.a] + i.b)
MULR, mulr = register('MULR', lambda mem, i: mem[i.a] * mem[i.b])
MULI, muli = register('MULI', lambda mem, i: mem[i.a] * i.b)
BANR, banr = register('BANR', lambda mem, i: mem[i.a] & mem[i.b])
BANI, bani = register('BANI', lambda mem, i: mem[i.a] & i.b)
BORR, borr = register('BORR', lambda mem, i: mem[i.a] | mem[i.b])
BORI, bori = register('BORI', lambda mem, i: mem[i.a] | i.b)
SETR, setr = register('SETR', lambda mem, i: mem[i.a])
SETI, seti = register('SETI', lambda _, i: i.a)
GTIR, gtir = register('GTIR', lambda mem, i: int(i.a > mem[i.b]))
GTRI, gtri = register('GTRI', lambda mem, i: int(mem[i.a] > i.b))
GTRR, gtrr = register('GTRR', lambda mem, i: int(mem[i.a] > mem[i.b]))
EQRI, eqri = register('EQRI', lambda mem, i: int(i.a == mem[i.b]))
EQIR, eqir = register('EQIR', lambda mem, i: int(mem[i.a] == i.b))
EQRR, eqrr = register('EQRR', lambda mem, i: int(mem[i.a] == mem[i.b]))


def check_all(instruction: Instruction, memory: Memory, expected: tuple, setup: tuple,
              possibilities: DefaultDict[int, Set[str]]):
    opcode = instruction.op
    count = 0
    for id, oper in operations:
        with memory.temp(setup):
            memory[instruction.c] = oper(memory, instruction)
            if memory == expected:
                possibilities[opcode].add(id)
                count += 1
    return count


# noinspection PyUnboundLocalVariable
def solve_part_1():
    possibilities = defaultdict(set)
    memory = Memory()
    before = after = False
    sample_instruction: Instruction = None
    sample_before_regs: tuple = None
    count = 0

    for line in read_lines():
        is_after = 'After' in line
        is_before = 'Before' in line
        is_sample = before or after or is_before or is_after

        if is_after:
            after = True
            before = False
        elif is_before:
            before = True
            after = False
        elif after and line.replace(' ', '').isnumeric():
            before = False
            after = False

        instruction = find_instruction(line)

        if is_before:
            sample_before_regs = tuple(instruction)
        elif is_after:
            count += check_all(sample_instruction, memory, extract_numbers(line), sample_before_regs,
                               possibilities) >= 3
        elif is_sample:
            sample_instruction = instruction

    return count


pprint(solve_part_1())
