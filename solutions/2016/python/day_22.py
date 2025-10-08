import re
import numpy as np

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
lines = open(os.path.join(INPUT_DIR, "2016_22.txt")).read().split('\n')

avail = []
used = []
nodes = {}
max_x = 0
max_y = 0
empty_pos = None

for line in lines[2:]:
    if not line:
        continue
    sizes = re.search(r'x(\d+)-y(\d+).+T\s+(\d+)T\s+(\d+)T\s+\d+%', line)
    if not sizes:
        continue
    x = int(sizes.group(1))
    y = int(sizes.group(2))
    usd = int(sizes.group(3))
    avl = int(sizes.group(4))
    
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    
    used.append(usd)
    avail.append(avl)
    nodes[(x, y)] = (usd, avl)
    
    if usd == 0:
        empty_pos = (x, y)

# Create grid based on actual dimensions
grid = [['.' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

# Mark nodes in grid
for (x, y), (usd, avl) in nodes.items():
    if usd > 100:
        grid[y][x] = '#'
    elif usd == 0:
        grid[y][x] = '_'

grid[0][max_x] = 'G'  # Goal data starts at top-right
grid[0][0] = 'F'  # We want to move it to top-left

uss = np.array(used)
avs = np.array(avail)

# Part 1: Count viable pairs
# A viable pair is any two nodes (A,B) where:
# - Node A is not empty (used > 0)
# - Nodes A and B are not the same node
# - The data on node A would fit on node B (A's used <= B's avail)
first_solution = 0
for i, u in enumerate(used):
    if u > 0:  # Node A is not empty
        for j, a in enumerate(avail):
            if i != j and u <= a:  # Different nodes and data fits
                first_solution += 1

# Part 2: Find minimum steps to move goal data
# The empty node is at empty_pos
# We need to move it to position adjacent to goal, then shuffle data

# Find position of wall (leftmost wall in row with walls)
wall_y = None
wall_left_x = max_x

for y in range(max_y + 1):
    has_wall = False
    for x in range(max_x + 1):
        if grid[y][x] == '#':
            has_wall = True
            wall_left_x = min(wall_left_x, x)
    if has_wall and wall_y is None:
        wall_y = y

# Strategy:
# 1. Move empty space around the wall to get to the goal position
# 2. Move goal data step by step to the target
start = empty_pos
goal = (max_x, 0)  # Position of goal data
target = (0, 0)    # Where we want goal data

def get_manhattan(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x2 - x1) + abs(y2 - y1)

# Move empty to position left of the wall, then up and around
# Empty needs to go around wall to reach the goal
steps = 0

# Move empty to the left of wall
if empty_pos[0] > wall_left_x - 1:
    steps += empty_pos[0] - (wall_left_x - 1)
    
# Move empty up to above the wall
steps += empty_pos[1]

# Move empty right to goal column
steps += max_x - (wall_left_x - 1)

# Now empty is adjacent to goal, shuffle goal to target
# Each move of goal requires 5 moves of empty (move around goal)
steps += 5 * (goal[0] - 1)

print(first_solution)
print(steps)
