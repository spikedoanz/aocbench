import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = [[int(x) for x in row.split()] for row in open(os.path.join(INPUT_DIR, "2017_02.txt")).readlines()]

print(sum(max(r)-min(r) for r in data))
print(sum(x//y for r in data for x in r for y in r if x != y and x % y == 0))
