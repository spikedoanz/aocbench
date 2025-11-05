import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_04.txt")).readlines()

def part1():
    from collections import Counter
    def solve(input):
      lower, upper = map(int, input[0].split("-"))
      n = 0
      for x in range(lower, upper):
        candidate = str(x)
        counts = Counter(candidate)
        twosame = max(counts.values()) >= 2
        increases = list(candidate) == sorted(candidate)
        if twosame and increases: n += 1
      return n
    return solve(data

def part2():
    def solve(input):
      lower, upper = map(int, input[0].split("-"))
      n = 0
    
      for x in range(lower, upper):
        candidate = str(x)
        counts = Counter(candidate)
        twosame = 2 in counts.values()
        increases = list(candidate) == sorted(candidate)
        if twosame and increases: n += 1
    
      return n
    

    from collections import Counter
    return solve(data

print(part1())
print(part2())
