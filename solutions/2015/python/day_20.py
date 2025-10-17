def solve(target, limit):
    houses = [1] * target
    for i in range(2, target):
        for j in range(min(target//i, limit)):
            houses[i*j] += i
        if houses[i] >= target:
            return i


import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
INPUT = int(open(os.path.join(INPUT_DIR, "2015_20.txt")).read().strip())
print(solve(INPUT//10, INPUT//10))
print(solve(INPUT//11, 50))
