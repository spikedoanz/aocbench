import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

from collections import defaultdict

with open(os.path.join(INPUT_DIR, '2019_09.txt')) as f:
    ns = list(map(int, f.read().split(',')))

def run(inp):
    p = defaultdict(int, enumerate(ns))
    i = 0
    base = 0
    while True:
        cmd = str(p[i]).zfill(5)
        opcode = int(cmd[3:])
        modes = {k: int(cmd[3 - k]) for k in (1, 2, 3)}
        addrs = {}
        for k in (1, 2, 3):
            try:
                if modes[k] == 0:
                    addrs[k] = p[i+k]
                elif modes[k] == 1:
                    addrs[k] = i+k
                elif modes[k] == 2:
                    addrs[k] = p[i+k]+base
            except IndexError:
                pass
        if opcode == 1:
            p[addrs[3]] = p[addrs[1]] + p[addrs[2]]
            i += 4
        elif opcode == 2:
            p[addrs[3]] = p[addrs[1]] * p[addrs[2]]
            i += 4
        elif opcode == 3:
            p[addrs[1]] = inp
            i += 2
        elif opcode == 4:
            print(p[addrs[1]])
            i += 2
        elif opcode == 5:
            i = p[addrs[2]] if p[addrs[1]] != 0 else i + 3
        elif opcode == 6:
            i = p[addrs[2]] if p[addrs[1]] == 0 else i + 3
        elif opcode == 7:
            p[addrs[3]] = int(p[addrs[1]] < p[addrs[2]])
            i += 4
        elif opcode == 8:
            p[addrs[3]] = int(p[addrs[1]] == p[addrs[2]])
            i += 4
        elif opcode == 9:
            base += p[addrs[1]]
            i += 2
        elif opcode == 99:
            return

def part1():
    run(1)

def part2():
    run(2)

print(part1())
print(part2())
