import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = [row.split() for row in open(os.path.join(INPUT_DIR, "2017_04.txt")).readlines()]

print(sum(1 for p in data if len(p) == len(set(p))))
print(sum(1 for p in data if len(p) == len(set([tuple(sorted(w)) for w in p]))))
