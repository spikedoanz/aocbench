import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_06.txt")) as f:
    data = f.read().strip()

groups = data.split('\n\n')

# Part one
print(sum(len(set(g.replace('\n', ''))) for g in groups))

# Part two
print(sum(len(set.intersection(*map(set, g.split('\n')))) for g in groups))