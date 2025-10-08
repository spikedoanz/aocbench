import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
e = d = v = i = n = 0
for c in open(os.path.join(INPUT_DIR, "2017_09.txt")).readline().strip():
    if d:
        d = 0
    elif c == '!':
        d = 1
    elif n:
        if c == '>':
            n = 0
        else:
            i += 1
    elif c == '{':
        e += 1
    elif c == '<':
        n = 1
    elif c == '}':
        v += e
        e -= 1

print(v)
print(i)
