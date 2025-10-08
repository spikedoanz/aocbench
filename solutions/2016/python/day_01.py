import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
directions = open(os.path.join(INPUT_DIR, "2016_01.txt")).readline().split(', ')

ROTATION = {
    'L': 1j,
    'R': -1j
}

current_direction = 1j
location = 0+0j

visited_locations = set()
part2 = None


def find_manhattan(loc):
    return int(abs(loc.real) + abs(loc.imag))


for instruction in directions:
    rot, dist = instruction[0], int(instruction[1:])
    current_direction *= ROTATION[rot]

    for _ in range(dist):
        location += current_direction
        if part2 is None and location in visited_locations:
            part2 = find_manhattan(location)
        else:
            visited_locations.add(location)

print(find_manhattan(location))
print(part2)
