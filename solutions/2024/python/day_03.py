import os
import re

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2024_03.txt")) as f:
    data = f.read()


def solve(part1):
    res = 0
    do = True
    for i, j, k in re.findall("(mul\((\d+),(\d+)\)|do\(\)|don't\(\))", data):
        if i == "don't()":
            do = False
        elif i == "do()":
            do = True
        else:
            if do or part1:
                res += int(j) * int(k)
    return res


# Part 1
print(solve(True))

# Part 2
print(solve(False))
