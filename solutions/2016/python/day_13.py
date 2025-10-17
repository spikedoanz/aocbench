from collections import deque

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
INPUT = int(open(os.path.join(INPUT_DIR, "2016_13.txt")).read().strip())
GOAL = (31, 39)
START = (1, 1)
DELTAS = ((1, 0), (-1, 0), (0, 1), (0, -1))

formula = lambda x, y: x*x + 3*x + 2*x*y + y + y*y + INPUT


def run_through_maze(second_part=False):
    que = deque([(START, 0)])
    seen = set()

    while que:
        (x, y), steps = que.popleft()

        if not second_part and (x, y) == GOAL:
            return steps
        if second_part and steps > 50:
            return len(seen)

        seen.add((x, y))

        for dx, dy in DELTAS:
            nx, ny = (x+dx, y+dy)
            if not ((nx, ny) in seen
                    or any(n < 0 for n in (nx, ny))
                    or bin(formula(nx, ny)).count('1') % 2):
                que.append(((nx, ny), steps+1))


print(run_through_maze())
print(run_through_maze('second'))
