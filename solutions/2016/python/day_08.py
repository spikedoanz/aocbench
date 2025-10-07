import numpy as np
# import matplotlib.pyplot as plt

instructions = open("inputs/2016_08.txt").read().split('\n')

lcd = np.zeros((6, 50))

for line in instructions:
    if line.startswith('rect'):
        width, height = map(int, line.split()[1].split('x'))
        lcd[:height, :width] = 1
    elif line.startswith('rotate'):
        _, ax, pos, _, shift = line.split()
        pos = int(pos.split('=')[1])
        shift = int(shift)
        if ax == 'row':
            lcd[pos] = np.roll(lcd[pos], shift)
        else:
            lcd[:, pos] = np.roll(lcd[:, pos], shift)

print(int(np.sum(lcd)))
print('\n'.join(' '.join('#' if on else ' ' for on in line) for line in lcd))

# plt.imshow(lcd, cmap='viridis')
# plt.show()
