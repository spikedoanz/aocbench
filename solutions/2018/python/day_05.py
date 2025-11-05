import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
line = open(os.path.join(INPUT_DIR, "2018_05.txt")).readline().strip()

def react(x):
    result = ['']
    for c in x:
        if c == result[-1].swapcase():
            result.pop()
        else:
            result.append(c)
    return ''.join(result)

# part 1
print(len(react(line)))

# part 2
print(min(len(react(line.replace(c, '').replace(c.upper(), '')))
    for c in set(line.lower())))