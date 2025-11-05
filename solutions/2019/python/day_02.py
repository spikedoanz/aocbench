import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, '2019_02.txt')) as f:
    p0 = list(map(int, f.read().split(',')))


def run(n1, n2):
    p = list(p0)
    i = 0
    p[1] = n1
    p[2] = n2
    while True:
        if p[i] == 1:
            p[p[i+3]] = p[p[i+1]] + p[p[i+2]]
        elif p[i] == 2:
            p[p[i+3]] = p[p[i+1]] * p[p[i+2]]
        elif p[i] == 99:
            return p[0]
        i += 4



def part1():
    return run(12, 2)



def part2():
    for n1 in range(100):
        for n2 in range(100):
            o = run(n1, n2)
            if o == 19690720:
                return 100 * n1 + n2

print(part1())
print(part2())
