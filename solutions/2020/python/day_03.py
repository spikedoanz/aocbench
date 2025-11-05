import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_03.txt")) as f:
    ls = [x.strip() for x in f.readlines()]


def count_trees(slope_x, slope_y):
    x = 0
    y = 0
    trees = 0
    while y < len(ls):
        trees += ls[y][x % len(ls[0])] == '#'
        x += slope_x
        y += slope_y
    return trees


# Part one
print(count_trees(3, 1))

# Part two
print(
    count_trees(1, 1) * count_trees(3, 1) * count_trees(5, 1)
    * count_trees(7, 1) * count_trees(1, 2)
)