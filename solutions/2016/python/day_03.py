from itertools import chain

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
puzzle = open(os.path.join(INPUT_DIR, "2016_03.txt")).readlines()

horizontal = [[int(value) for value in row.split()] for row in puzzle]
vertical = list(chain.from_iterable(zip(*horizontal)))


def is_triangle(sides):
    a, b, c = sorted(sides)
    return a + b > c


def find_triangles(candidates, second_part=False):
    if not second_part:
        return sum(is_triangle(row) for row in candidates)
    else:
        return sum(is_triangle(candidates[i:i+3])
                   for i in range(0, len(candidates)-2, 3))


print(find_triangles(horizontal))
print(find_triangles(vertical, True))
