import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
first_row = open(os.path.join(INPUT_DIR, "2016_18.txt")).read()


def count_safes(row, total_lines):
    safe = 0
    for i in range(total_lines):
        if i == 40:
            first_solution = safe
        safe += row.count('.')
        old = '.' + row + '.'
        row = ''
        for left, right in zip(old, old[2:]):
            row += '^' if left != right else '.'
    return first_solution, safe


first, second = count_safes(first_row, 400000)

print(first)
print(second)
