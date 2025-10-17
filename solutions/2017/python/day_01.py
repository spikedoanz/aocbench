import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
data = open(os.path.join(INPUT_DIR, "2017_01.txt")).readline().strip()

ds = [int(d) for d in data]
n = len(ds)

print(sum(d for i, d in enumerate(ds) if d == ds[(i+1) % n]))
print(sum(d for i, d in enumerate(ds) if d == ds[(i+n//2) % n]))
