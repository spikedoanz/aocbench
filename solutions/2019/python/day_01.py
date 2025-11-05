import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, '2019_01.txt')) as f:
    ns = list(map(int, (x.strip() for x in f.readlines())))


def fuel(m):
    return m // 3 - 2



def part1():
    return sum(map(fuel, ns))


def part2():
    total = 0
    for n in ns:
        while True:
            n = fuel(n)
            if n <= 0:
                break
            total += n
    return total

print(part1())
print(part2())
