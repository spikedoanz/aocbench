import os
from sympy.ntheory.residue_ntheory import discrete_log

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_25.txt")) as f:
    lines = f.read().strip().split('\n')

card_pub = int(lines[0])
door_pub = int(lines[1])
modulus = 20201227

print(pow(door_pub, discrete_log(modulus, card_pub, 7), modulus))