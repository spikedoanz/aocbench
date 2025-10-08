import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
with open(os.path.join(INPUT_DIR, "2016_12.txt"), 'r') as infile:
    instructions = infile.read().splitlines()


def execute(c):
    register = {'a': 0, 'b': 0, 'c': c, 'd': 0}
    interpret = lambda val: int(val) if val.isdigit() else register[val]
    i = 0

    while i < len(instructions):
        instr, x, *y = instructions[i].split()
        y = y[0] if y else None

        if instr == 'cpy':
            register[y] = interpret(x)

        if instr == 'inc':
            register[x] += 1

        if instr == 'dec':
            register[x] -= 1

        if instr == 'jnz':
            if interpret(x) != 0:
                i += int(y)
                continue

        i += 1
    return register['a']


print(execute(c=0))
print(execute(c=1))
