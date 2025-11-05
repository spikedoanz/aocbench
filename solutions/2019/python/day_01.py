import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_01.txt")).readlines()

def part1():
    sum_val = 0
    for line in lines:
        sum_val += int(line) // 3 - 2
    return sum_val

def part2():
    def fuel_for(input_val):
        output = input_val // 3 - 2
        return 0 if output <= 0 else output + fuel_for(output)
    
    sum_val = 0
    for line in lines:
        sum_val += fuel_for(int(line))
    return sum_val

print(part1())
print(part2())