import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
data = open(os.path.join(INPUT_DIR, "2022_01.txt")).read().strip()

groups = data.split("\n\n")
group_sums = [sum(map(int, group.split("\n"))) for group in groups]

# Part 1
print(max(group_sums))

# Part 2
print(sum(sorted(group_sums)[-3:]))
