import os
from itertools import islice
import string

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
ls = [x.strip() for x in open(os.path.join(INPUT_DIR, "2022_03.txt")).readlines()]

score = (" " + string.ascii_lowercase + string.ascii_uppercase).index

# Part 1
s = 0
for l in ls:
    mid = len(l) // 2
    p1, p2 = l[:mid], l[mid:]
    (o,) = set(p1) & set(p2)
    s += score(o)
print(s)

# Part 2
sets = map(set, ls)
s = 0
for _ in range(len(ls) // 3):
    (o,) = set.intersection(*islice(sets, 3))
    s += score(o)
print(s)
