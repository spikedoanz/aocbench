import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, '2019_03.txt')) as f:
    ls = [l.split(',') for l in f.readlines()]


def make_wire(l):
    c = 0
    i = 1
    directions = {'R': 1j, 'L': -1j, 'U': 1, 'D': -1}
    covered = {}
    for d in l:
        direction = directions[d[0]]
        for _ in range(int(d[1:])):
            c += direction
            if c not in covered:
                covered[c] = i
            i += 1
    return covered


wire1 = make_wire(ls[0])
wire2 = make_wire(ls[1])
crossings = set(wire1) & set(wire2)


def part1():
    return int(min(abs(c.real) + abs(c.imag) for c in crossings))


def part2():
    return min(wire1[c] + wire2[c] for c in crossings)

print(part1())
print(part2())
