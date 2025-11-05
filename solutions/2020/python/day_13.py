import os
from itertools import count
from sympy.ntheory.modular import solve_congruence

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_13.txt")) as f:
    ls = [line.strip() for line in f.readlines()]

earliest = int(ls[0])
bus_times = [(-i, int(x)) for i, x in enumerate(ls[1].split(',')) if x != 'x']
_, busses = zip(*bus_times)

# Part one
print(next((time - earliest)*bus
           for time in count(earliest) for bus in busses
           if time % bus == 0))

# Part two
print(solve_congruence(*bus_times)[0])