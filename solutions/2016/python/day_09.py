import re

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
compressed = open(os.path.join(INPUT_DIR, "2016_09.txt")).read()

pattern = re.compile(r'\((\d+)x(\d+)\)')

def unzip(s, second_part=False):
    parens = pattern.search(s)
    if not parens:
        return len(s)
    length = int(parens.group(1))
    times = int(parens.group(2))
    start = parens.start() + len(parens.group())
    count = unzip(s[start:start+length], True) if second_part else length

    return (len(s[:parens.start()])
            + times * count
            + unzip(s[start+length:], second_part))


print(unzip(compressed))
print(unzip(compressed, second_part=True))
