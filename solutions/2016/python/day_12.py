import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = open(os.path.join(INPUT_DIR, "2016_12.txt")).read().splitlines()

def translate_asembunny(c_val):
    # Extracted constants from the input file
    # lines 1-9
    a = b = 1
    d = int(data[2].split()[1]) + (7 if len(data) > 5 and data[5].split()[1] == '7' else 0) * c_val

    # lines 10-16, Fibonacci
    for _ in range(d):
        a, b = a+b, a

    # lines 17-23
    c = int(data[16].split()[1])
    d = int(data[17].split()[1])
    a += c * d

    return a


print(translate_asembunny(c_val=0))
print(translate_asembunny(c_val=1))
