import os
from collections import Counter

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2024_01.txt")) as f:
    ls = f.read().strip().split("\n")

l1, l2 = zip(*[map(int, x.split()) for x in ls])

# Part 1
print(sum(abs(a - b) for a, b in zip(sorted(l1), sorted(l2))))

# Part 2
cs = Counter(l2)
print(sum(x * cs[x] for x in l1))
