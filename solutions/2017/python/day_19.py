import re

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = [[c if c != ' ' else 0 for c in x.strip('\n')]
        for x in open(os.path.join(INPUT_DIR, "2017_19.txt")).readlines()]

dx, dy = 0, 1
y = 0
x = data[y].index('|')
seen = []
steps = 0
while data[y][x]:
    seen.extend(re.findall('[A-Z]', data[y][x]))
    steps += 1
    if data[y][x] == '+':
        if dx:
            dx, dy = 0, 1 if data[y+1][x] else -1
        else:
            dx, dy = 1 if data[y][x+1] else -1, 0
    x += dx
    y += dy

print(''.join(seen))
print(steps)
