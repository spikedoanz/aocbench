import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

import numpy as np


with open(os.path.join(INPUT_DIR, '2019_08.txt')) as f:
    layers = np.array(list(f.read().strip())).reshape(-1, 6*25)


def part1():
    layer = layers[(layers == '0').sum(1).argmin()]
    return (layer == '1').sum() * (layer == '2').sum()


def part2():
    visible = np.argmax(layers != '2', 0)
    image = layers[(visible, range(len(visible)))].reshape(6, 25)
    return '\n'.join(''.join(x).replace('0', ' ') for x in image)

print(part1())
print(part2())
