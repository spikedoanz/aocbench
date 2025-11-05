import os
from functools import cache

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2024_19.txt")) as f:
    ls = f.read().strip().split("\n")

stripes, _, *patterns = ls
stripes = stripes.split(", ")


@cache
def is_possible(pattern, op):
    return not pattern or op(
        is_possible(pattern[len(stripe) :], op)
        for stripe in stripes
        if pattern.startswith(stripe)
    )


# Part 1 + 2
for op in any, sum:
    print(sum(is_possible(pattern, op) for pattern in patterns))
