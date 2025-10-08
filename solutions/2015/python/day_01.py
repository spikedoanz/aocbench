import os
from itertools import accumulate

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = open(os.path.join(INPUT_DIR, "2015_01.txt")).readline()

travel = lambda acc, c: acc + (1 if c == '(' else -1)
floors_visited = list(accumulate(data, travel, initial=0))

print(floors_visited[-1])
print(next(i for i, floor in enumerate(floors_visited) if floor < 0))
