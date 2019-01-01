import re
from dataclasses import dataclass

from typing import List


@dataclass
class Marker:
    x: int
    y: int
    vx: int
    vy: int


FILE = 'example.txt'

with open(FILE) as f:
    markers = tuple(Marker(*re.findall(r'-?\d+', line)) for line in f)

print(markers)
