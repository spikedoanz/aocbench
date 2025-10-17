def solve(digits, times):
    digits = list(map(int, digits))
    for _ in range(times):
        d = digits[0]
        reps = 0
        new_digits = []
        for digit in digits:
            if digit == d: reps += 1
            else:
                new_digits.append(reps)
                new_digits.append(d)
                d = digit
                reps = 1
        new_digits.append(reps)
        new_digits.append(d)
        digits = new_digits
    return digits


import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
INPUT = open(os.path.join(INPUT_DIR, "2015_10.txt")).read().strip()

print(len(first := solve(INPUT, 40)))
print(len(solve(first, 10)))
