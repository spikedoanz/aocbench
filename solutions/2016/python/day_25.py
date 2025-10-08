import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))

def execute(a):
    instructions = open(os.path.join(INPUT_DIR, "2016_25.txt")).read().splitlines()

    register = {'a': a, 'b': 0, 'c': 0, 'd': 0}
    line = 0
    transmitted = [1]

    interpret = lambda val: register[val] if val.isalpha() else int(val)

    while line < len(instructions):
        instr, x, *y = instructions[line].split()
        y = y[0] if y else None

        if instr == 'out':
            x_ = interpret(x)
            if x_ not in {0, 1} or x_ == transmitted[-1]:
                return False
            else:
                transmitted.append(x_)
            if len(transmitted) > 10:
                return True

        if instr == 'cpy':
            register[y] = interpret(x)

        if instr == 'inc':
            register[x] += 1

        if instr == 'dec':
            register[x] -= 1

        if instr == 'jnz':
            if interpret(x) != 0:
                line += interpret(y)
                continue

        line += 1


i = 0
while True:
    result = execute(i)
    if result:
        break
    i += 1

print(i)
