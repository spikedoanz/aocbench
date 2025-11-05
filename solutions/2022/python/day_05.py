import os
import re

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
ls = open(os.path.join(INPUT_DIR, "2022_05.txt")).readlines()

ns = [list(map(int, re.findall("\d+", x))) for x in ls[10:]]

stacks = [
    "BWN",
    "LZSPTDMB",
    "QHZWR",
    "WDVJZR",
    "SHMB",
    "LGNJHVPB",
    "JQZFHDLS",
    "WSFJGQB",
    "ZWMSCDJ",
]


def solve(stacks, part1):
    stacks = list(stacks)
    for amount, from_stack, to_stack in ns:
        top = stacks[from_stack - 1][-amount:]
        if part1:
            top = top[::-1]
        stacks[from_stack - 1] = stacks[from_stack - 1][:-amount]
        stacks[to_stack - 1] += top
    return "".join(s[-1] for s in stacks)


# Part 1
print(solve(stacks, True))

# Part 2
print(solve(stacks, False))
