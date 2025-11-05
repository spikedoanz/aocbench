import os
from collections import Counter

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2024_11.txt")) as f:
    stones = Counter(map(int, f.read().split()))

for blinks in range(1, 76):
    new_stones = Counter()
    for n, num_stone in stones.items():
        mid, rem = divmod(len(str(n)), 2)
        if n == 0:
            new_stones[1] += num_stone
        elif rem:
            new_stones[2024 * n] += num_stone
        else:
            for m in divmod(n, 10**mid):
                new_stones[m] += num_stone
    stones = new_stones
    if blinks in (25, 75):
        print(sum(new_stones.values()))
