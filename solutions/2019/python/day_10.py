import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

from cmath import phase

with open(os.path.join(INPUT_DIR, '2019_10.txt')) as f:
    ls = f.readlines()

asteroids = set(m + n*1j
                for n, row in enumerate(ls)
                for m, col in enumerate(row) if col == '#')


visible = {a: set(phase((b-a)/1j) for b in asteroids if b != a)
           for a in asteroids}
station, v = max(visible.items(), key=lambda x: len(x[1]))

def part1():
    return len(v)

def part2():
    d = sorted((phase((b-station)/1j), abs(b-station), b) for b in asteroids if b != station)
    last_phase = None
    c = 0
    for this_phase, _, b in d:
        if this_phase != last_phase:
            last_phase = this_phase
            c += 1
            if c == 200:
                return int(b.real*100 + b.imag)

print(part1())
print(part2())
