import os
from collections import defaultdict
import re

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

ids = defaultdict(set)
for line in open(os.path.join(INPUT_DIR, "2018_03.txt")):
    id, x, y, w, h = map(int, re.findall(r'\d+', line))
    for j in range(y, y + h):
        for i in range(x, x + w):
            ids[(i, j)].add(id)

# part 1
print(sum(len(x) > 1 for x in ids.values()))

# part 2
all_ids = set()
invalid_ids = set()
for x in ids.values():
    all_ids |= x
    if len(x) > 1:
        invalid_ids |= x

print(all_ids - invalid_ids)