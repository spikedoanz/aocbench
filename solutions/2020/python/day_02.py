import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_02.txt")) as f:
    ws = [x.strip().split() for x in f.readlines()]

# Part one
valid = 0
for w in ws:
    lo, hi = list(map(int, w[0].split('-')))
    char = w[1][0]
    valid += lo <= w[2].count(char) <= hi
print(valid)

# Part two
valid = 0
for w in ws:
    a, b = list(map(int, w[0].split('-')))
    char = w[1][0]
    valid += (w[2][a - 1] == char) ^ (w[2][b - 1] == char)
print(valid)