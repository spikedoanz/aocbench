import os
import re

from lark import Lark

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

with open(os.path.join(INPUT_DIR, "2020_19.txt")) as f:
    data = f.read()

rules, messages = data.split('\n\n')
messages = messages.split()


def solve(rules):
    rules = 'start: t0\n' + re.sub(r'(\d+)', r't\1', rules)
    parser = Lark(rules)
    valid = len(messages)
    for message in messages:
        try:
            parser.parse(message)
        except:
            valid -= 1
    return valid


# Part one
print(solve(rules))

# Part two
rules = rules\
    .replace('8: 42', '8: 42 | 42 8')\
    .replace('11: 42 31', '11: 42 31 | 42 11 31')
print(solve(rules))