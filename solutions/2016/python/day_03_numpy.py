import numpy as np

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
in_ = np.loadtxt(os.path.join(INPUT_DIR, '2016_03.txt'))

def find_triangles(arr):
    arr.sort(axis=1)
    return sum(np.sum(arr[:, :2], axis=1) > arr[:, 2])

print(find_triangles(in_.copy()))
print(find_triangles(in_.T.reshape(-1, 3)))
