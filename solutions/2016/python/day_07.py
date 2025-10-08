import re

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
addresses = open(os.path.join(INPUT_DIR, "2016_07.txt")).readlines()

addresses_separated = [re.split(r'\[|\]', line.strip()) for line in addresses]

supernet = [' '.join(line[::2]) for line in addresses_separated]
hypernet = [' '.join(line[1::2]) for line in addresses_separated]


def is_abba(line):
    return any(a+b == d+c and a != b
               for a, b, c, d in zip(line, line[1:], line[2:], line[3:]))

def is_ababab(sup, hyp):
    return any(a == c and a != b and b+a+b in hyp
               for a, b, c in zip(sup, sup[1:], sup[2:]))


first_solution = sum(is_abba(sup) and not is_abba(hyp)
                     for sup, hyp in zip(supernet, hypernet))

second_solution = sum(is_ababab(sup, hyp)
                      for sup, hyp in zip(supernet, hypernet))


print(first_solution)
print(second_solution)
