import os
from itertools import combinations
import numpy as np

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_01.txt")) as f:
    ns = list(map(int, (x.strip() for x in f.readlines())))

# Part one
for a in combinations(ns, 2):
    if sum(a) == 2020:
        print(np.product(a))
        break

# Part two
for a in combinations(ns, 3):
    if sum(a) == 2020:
        print(np.product(a))
        break