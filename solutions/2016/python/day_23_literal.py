import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))

def execute(a):
    with open(os.path.join(INPUT_DIR, "2016_23.txt"), 'r') as infile:
        instructions = infile.read().splitlines()

    register = {'a': a, 'b': 0, 'c': 0, 'd': 0}
    interpret = lambda val: register[val] if val.isalpha() else int(val)
    i = 0

    def toggler(pos):
        line = instructions[pos].split()
        if len(line) == 2:
            line[0] = 'dec' if line[0] == 'inc' else 'inc'
        else:
            line[0] = 'cpy' if line[0] == 'jnz' else 'jnz'
        return ' '.join(line)

    def increaser(pos, value=1):
        register[pos] += value

    while i < len(instructions):
        instr, x, *y = instructions[i].split()
        y = y[0] if y else None

        # optimization for instruction lines 5-10
        if i == 4:
            register['a'] += register['d'] * register['b']
            register['c'] = 0
            register['d'] = 0
            i += 6
            continue

        # optimization for instruction lines 21-26
        # line 21 = cpy 87 d
        # line 23 = dec d
        if i == 20:
            register['a'] += 87 * register['c']
            break

        if instr == 'cpy':
            if isinstance(y, int):
                i += 1
                continue
            register[y] = interpret(x)

        if instr == 'inc':
            increaser(x)

        if instr == 'dec':
            increaser(x, -1)

        if instr == 'jnz':
            if interpret(x) != 0:
                i += interpret(y)
                continue

        if instr == 'tgl':
            pos = i + interpret(x)
            if 0 <= pos < len(instructions):
                instructions[pos] = toggler(pos)

        i += 1
    return register['a']


print(execute(a=7))
print(execute(a=12))
