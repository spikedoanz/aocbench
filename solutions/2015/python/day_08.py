import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = open(os.path.join(INPUT_DIR, "2015_08.txt")).read().splitlines()

print(sum(len(line) - len(eval(line)) for line in data))
print(sum(line.count(r'"') + line.count('\\') + 2 for line in data))
