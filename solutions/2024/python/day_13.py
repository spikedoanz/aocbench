import os
import re
import z3

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2024_13.txt")) as f:
    groups = [
        list(map(int, re.findall("\\d+", g))) for g in f.read().strip().split("\n\n")
    ]


def price(ax, ay, bx, by, tx, ty, offset=0):
    tx += offset
    ty += offset
    a = z3.Int("a")
    b = z3.Int("b")
    s = z3.Solver()
    s.add(a * ax + b * bx == tx)
    s.add(a * ay + b * by == ty)
    s.add(a >= 0)
    s.add(b >= 0)
    if s.check() == z3.sat:
        m = s.model()
        return 3 * m[a].as_long() + m[b].as_long()
    return 0


# Part 1
print(sum(price(*g) for g in groups))

# Part 2
print(sum(price(*g, 10000000000000) for g in groups))
