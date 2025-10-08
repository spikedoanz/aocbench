import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
d = int(open(os.path.join(INPUT_DIR, "2017_17.txt")).readline().strip())

b, p, n = [0], 0, 0

for i in range(1, 2018):
    p = 1 + (p + d) % i
    b.insert(p, i)
print(b[p+1 % len(b)])

for i in range(1, 50000001):
    p = 1 + (p + d) % i
    if p == 1:
        n = i
print(n)
