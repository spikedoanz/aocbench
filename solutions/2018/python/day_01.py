import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2018_01.txt")).readlines()

def part1():
    return sum(map(int, lines))

def part2():
    f = 0
    seen = {f}
    while True:
        for line in lines:
            f += int(line)
            if f in seen:
                return f
            seen.add(f)

print(part1())
print(part2())