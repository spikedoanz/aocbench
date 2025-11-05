import os
from collections import deque
import re

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

num_players, num_marbles = map(int,
    re.findall(r'\d+', open(os.path.join(INPUT_DIR, "2018_09.txt")).readline()))

def solve(num_players, num_marbles):
    d = deque([0])
    scores = [0] * num_players
    for m in range(1, num_marbles + 1):
        if m % 23 == 0:
            d.rotate(7)
            scores[m % num_players] += m + d.pop()
            d.rotate(-1)
        else:
            d.rotate(-1)
            d.append(m)
    return max(scores)

print(solve(num_players, num_marbles))
print(solve(num_players, num_marbles * 100))