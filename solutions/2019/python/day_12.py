import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

from itertools import count
import re

import numpy as np


with open(os.path.join(INPUT_DIR, '2019_12.txt')) as f:
    ns = np.array([list(map(int, re.findall(r'-?\d+', x))) for x in f.readlines()])

state0 = np.stack([ns, np.zeros((4, 3), dtype=int)])


def part1():
    state = state0.copy()
    for _ in range(1000):
        state[1] += np.sign(state[0] - state[0, :, None]).sum(1)
        state[0] += state[1]
    return abs(state).sum(2).prod(0).sum()



def part2():
    # Here, we first of all make use of the fact that the three directions
    # are independent, so we need to find cycles for each of them and use
    # that to determine the overall cycle length. Moreover, since the process
    # is reversible, the cycles will start at time 0, and the overall cycle
    # length is simply the lowest common multiple of all of them.
    def find_axis_cycle_length(ax):
        state_ax = state0[:, :, ax].copy()
        for i in count(1):
            state_ax[1] += np.sign(state_ax[0] - state_ax[0, :, None]).sum(1)
            state_ax[0] += state_ax[1]
            if np.array_equal(state_ax, state0[:, :, ax]):
                return i


    return np.lcm.reduce(list(map(find_axis_cycle_length, range(3))))

print(part1())
print(part2())
