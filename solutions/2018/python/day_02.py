import os
from collections import Counter

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = [x.strip() for x in open(os.path.join(INPUT_DIR, "2018_02.txt")).readlines()]

def part1():
    has2 = 0
    has3 = 0
    for line in lines:
        c = Counter(line).values()
        has2 += 2 in c
        has3 += 3 in c
    return has2 * has3

def part2():
    for line1 in lines:
        for line2 in lines:
            x = ''.join(a for a, b in zip(line1, line2) if a == b)
            if len(x) == len(line1) - 1:
                return x

print(part1())
print(part2())