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
        return repr(self.as_list)


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


ADDI = 'addi'
ADDR = 'addr'

MULI = 'muli'
MULR = 'mulr'

BANI = 'bani'
BANR = 'banr'

BORI = 'bori'
BORR = 'borr'

SETR = 'setr'
SETI = 'seti'

GTIR = 'gtir'
GTRI = 'gtri'
GTRR = 'gtrr'

EQIR = 'eqir'
EQRI = 'eqri'
EQRR = 'eqrr'


def check_all(instruction: Instruction, memory: Memory, expected: tuple, setup: tuple,
              possibilities: DefaultDict[int, Set[str]]):
    opcode = instruction.op
    mem_temp = partial(memory.temp, setup)
    count = 0

    def check(id):
        nonlocal count
        if memory == expected:
            possibilities[opcode].add(id)
            count += 1

    # region operations

    # MULR
    with mem_temp():
        memory[instruction.c] = memory[instruction.a] * memory[instruction.b]
        check(MULR)

    # MULI
    with mem_temp():
        memory[instruction.c] = memory[instruction.a] * instruction.b
        check(MULI)

    # ADDR
    with mem_temp():
        memory[instruction.c] = memory[instruction.a] + memory[instruction.b]
        check(ADDR)

    # ADDI
    with mem_temp():
        memory[instruction.c] = memory[instruction.a] + instruction.b
        check(ADDR)

    # BANR - binary AND
    with mem_temp():
        memory[instruction.c] = memory[instruction.a] & memory[instruction.b]
        check(BANR)

    # BANI - binary AND
    with mem_temp():
        memory[instruction.c] = memory[instruction.a] & instruction.b
        check(BANI)

    # BORR - binary OR
    with mem_temp():
        memory[instruction.c] = memory[instruction.a] | memory[instruction.b]
        check(BORR)

    # BORI - binary OR
    with mem_temp():
        memory[instruction.c] = memory[instruction.a] | instruction.b
        check(BORI)

    # SETI
    with mem_temp():
        memory[instruction.c] = instruction.a
        check(SETI)

    # SETR
    with mem_temp():
        memory[instruction.c] = memory[instruction.a]
        check(SETR)

    # GTIR
    with mem_temp():
        memory[instruction.c] = int(instruction.a > memory[instruction.b])
        check(GTIR)

    # GTRI
    with mem_temp():
        memory[instruction.c] = int(memory[instruction.a] > instruction.b)
        check(GTRI)

    # GTRR
    with mem_temp():
        memory[instruction.c] = int(memory[instruction.a] > memory[instruction.b])
        check(GTRR)

    # EQIR
    with mem_temp():
        memory[instruction.c] = int(instruction.a == memory[instruction.b])
        check(EQIR)

    # EQRI
    with mem_temp():
        memory[instruction.c] = int(memory[instruction.a] == instruction.b)
        check(EQRI)

    # EQRR
    with mem_temp():
        memory[instruction.c] = int(memory[instruction.a] == memory[instruction.b])
        check(EQRR)

    # endregion
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
            expected = extract_numbers(line)
            count += check_all(sample_instruction, memory, expected, sample_before_regs, possibilities) >= 3
        elif is_sample:
            sample_instruction = instruction

    return count


pprint(solve_part_1())
