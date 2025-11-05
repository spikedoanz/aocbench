import os
from collections import defaultdict
from itertools import count

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_15.txt")) as f:
    ns = list(map(int, f.read().split(',')))


def solve(iteration):
    d = defaultdict(list)
    for i in count(1):
        if i <= len(ns):
            new = ns[i-1]
        elif len(d[last_spoken]) == 1:
            new = 0
        else:
            new = d[last_spoken][-1] - d[last_spoken][-2]
        if i == iteration:
            return new
        d[new].append(i)
        last_spoken = new


# Part one
print(solve(2020))

# Part two
print(solve(30_000_000))