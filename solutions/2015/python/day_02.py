from itertools import starmap


import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
data = open(os.path.join(INPUT_DIR, "2015_02.txt")).read().splitlines()
dimensions = [sorted(map(int, line.split('x'))) for line in data]

paper =  lambda a, b, c: 3*a*b + 2*b*c + 2*c*a
ribbon = lambda a, b, c: 2*a + 2*b + a*b*c

print(sum(starmap(paper, dimensions)))
print(sum(starmap(ribbon, dimensions)))
