import os
import re

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_05.txt")) as f:
    ls = [x.strip() for x in f.readlines()]


def binary(w):
    w = re.sub('[FL]', '0', w)
    w = re.sub('[BR]', '1', w)
    return int(w, 2)


# Part one
print(max(map(binary, ls)))

# Part two
all_ids = list(map(binary, ls))
for seat in sorted(all_ids):
    if seat + 1 not in all_ids and seat + 2 in all_ids:
        print(seat + 1)
        break