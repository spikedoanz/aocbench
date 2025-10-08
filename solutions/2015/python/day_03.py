def solve(data, players=1):
    directions = {'^': -1j, 'v': +1j, '<': -1, '>': 1}
    locations = [0] * players
    visited = {0}
    for i, d in enumerate(data):
        locations[i % players] += directions[d]
        visited |= {locations[i % players]}
    return len(visited)


import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = open(os.path.join(INPUT_DIR, "2015_03.txt")).readline()

print(solve(data))
print(solve(data, 2))