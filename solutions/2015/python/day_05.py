is_nice_1 = lambda s: (
    sum(c in 'aeiou' for c in s) >= 3 and
    any(a == b for a, b in zip(s, s[1:])) and
    all(f not in s for f in ('ab', 'cd', 'pq', 'xy')))

is_nice_2 = lambda s: (
    any(s[i:i+2] in s[:i] for i in range(len(s)-1)) and
    any(a == b for a, b in zip(s, s[2:])))


import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
data = open(os.path.join(INPUT_DIR, "2015_05.txt")).read().splitlines()

print(sum(map(is_nice_1, data)))
print(sum(map(is_nice_2, data)))
