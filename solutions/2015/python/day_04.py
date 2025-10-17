import os
from hashlib import md5
from itertools import count


def solve(target, start=1):
    for i in count(start):
        m = md5(f"{INPUT}{i}".encode()).hexdigest()
        if m.startswith(target): return i


INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
INPUT = open(os.path.join(INPUT_DIR, "2015_04.txt")).read().strip()

print(solve(5*'0'))
print(solve(6*'0'))