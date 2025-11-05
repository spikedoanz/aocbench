import os
from itertools import count

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
data = open(os.path.join(INPUT_DIR, "2022_06.txt")).read()


def solve(length):
    return next(i for i in count() if len(set(data[i - length : i])) == length)


# Part 1
print(solve(4))

# Part 2
print(solve(14))
