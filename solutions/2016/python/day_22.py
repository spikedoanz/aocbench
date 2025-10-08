import re
import numpy as np

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
lines = open(os.path.join(INPUT_DIR, "2016_22.txt")).read().split('\n')

avail = []
used = []
grid = [['.' for _ in range(33)] for _ in range(30)]

for line in lines[2:]:
    sizes = re.search(r'x(\d+)-y(\d+).+T\s+(\d+)T\s+(\d+)T\s+\d+%', line)
    x = int(sizes.group(1))
    y = int(sizes.group(2))
    usd = int(sizes.group(3))
    avl = int(sizes.group(4))
    used.append(usd)
    avail.append(avl)
    if usd > 100:
        grid[y][x] = '#'
    elif usd == 0:
        grid[y][x] = '_'

grid[0][-1] = 'G'
grid[0][0] = 'F'


uss = np.array(used)
first_solution = sum((uss <= 94) & (uss > 0))

start = (len(grid)-1, grid[-1].index('_'))
wall = (len(grid)-3, grid[-3].index('#')-1)
goal = (0, len(grid[0])-1)
finish = (0, 0)

def get_manhattan(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x2 - x1) + abs(y2 - y1)

steps = get_manhattan(start, wall)
steps += get_manhattan(wall, goal)
steps += 5 * (goal[1] - 1)

print(first_solution)
print(steps)
