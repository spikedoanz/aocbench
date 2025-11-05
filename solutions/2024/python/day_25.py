import os
from itertools import combinations

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2024_25.txt")) as f:
    gs = f.read().strip().split("\n\n")

# Part 1
print(
    sum(
        not any(x1 == x2 == "#" for x1, x2 in zip(g1, g2))
        for g1, g2 in combinations(gs, 2)
    )
)
