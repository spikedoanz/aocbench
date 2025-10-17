import itertools

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
ls = dict([int(y) for y in x.strip().split(': ')] for x in open(os.path.join(INPUT_DIR, "2017_13.txt")).readlines()]
h = lambda d: [i*ls[i] for i in ls if (i+d) % (ls[i]*2-2) == 0]

print(sum(h(0)))
print(next(d for d in itertools.count(0) if not h(d)))
