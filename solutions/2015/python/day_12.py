import json
import re


numbers = re.compile(r"-?\d+")

def find_sum(jason):
    if type(jason) is int:
        return jason
    if type(jason) is dict:
        if "red" in jason.values(): return 0
        else: return sum(map(find_sum, jason.values()))
    if type(jason) is list:
        return sum(map(find_sum, jason))
    else: return 0


import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
data = open(os.path.join(INPUT_DIR, "2015_12.txt")).read()
j = json.loads(data)

print(sum(map(int, re.findall(numbers, data))))
print(find_sum(j))
