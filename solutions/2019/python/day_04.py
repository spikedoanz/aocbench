import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

start = 245182
end = 790572


def two_adjacent(d, part_one):
    s = str(d)
    return any(s[i] == s[i+1] and
               (part_one or
                ((i == len(s) - 2 or s[i+1] != s[i+2]) and (i == 0 or s[i-1] != s[i])))
               for i in range(len(s) - 1))


def increasing(d):
    s = str(d)
    return sorted(s) == list(s)



def part1():
    return sum(two_adjacent(d, True) and increasing(d) for d in range(start, end))


def part2():
    return sum(two_adjacent(d, False) and increasing(d) for d in range(start, end))

print(part1())
print(part2())
