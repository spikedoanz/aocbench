import numpy as np
import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
instructions = open(os.path.join(INPUT_DIR, "2016_08.txt")).read().strip().split('\n')

# Initialize 6x50 LCD display (all pixels off)
lcd = np.zeros((6, 50), dtype=int)

# Process each instruction
for line in instructions:
    if line.startswith('rect'):
        # Parse "rect AxB" - turn on rectangle
        dimensions = line.split()[1]
        width, height = map(int, dimensions.split('x'))
        lcd[:height, :width] = 1
        
    elif line.startswith('rotate row'):
        # Parse "rotate row y=A by B" - shift row right
        parts = line.split()
        row = int(parts[2].split('=')[1])
        shift = int(parts[4])
        lcd[row] = np.roll(lcd[row], shift)
        
    elif line.startswith('rotate column'):
        # Parse "rotate column x=A by B" - shift column down
        parts = line.split()
        col = int(parts[2].split('=')[1])
        shift = int(parts[4])
        lcd[:, col] = np.roll(lcd[:, col], shift)

# Part 1: Count lit pixels
print(int(np.sum(lcd)))

for row in lcd:
    # Use '#' for lit pixels and '.' or space for unlit ones
    # No spaces between characters for better readability
    print(''.join('#' if pixel else '.' for pixel in row))
