import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_08.txt")).readlines()

def part1():
    from collections import defaultdict
    def solve(data):
      width, height = 25, 6
      i = 0
      checksums = {}
      while i < len(data):
        colors = defaultdict(lambda: 0)
        for _ in range(width * height):
          colors[data[i]] += 1
          i += 1
        checksums[colors[0]] = colors[1] * colors[2]
      return checksums[min(checksums.keys())]
    return solve(data

def part2():
    def solve(data):
      width, height = 25, 6
      i = 0
      matrix = [[2 for x in range(height)] for y in range(width)]
    
      while i < len(data):
        for h in range(height):
          for w in range(width):
            if matrix[w][h] == 2 and data[i] < 2:
              matrix[w][h] = data[i]
            i += 1
    
      for h in reversed(range(height)):
        line = ""
        for w in reversed(range(width)):
          if matrix[width - 1 - w][height - 1 - h] == 0: line += '░' # black
          if matrix[width - 1 - w][height - 1 - h] == 1: line += '█' # white
          if matrix[width - 1 - w][height - 1 - h] == 2: line += ' ' # transparent
        print(line)
    
      return 'read the answer above in ascii art!'
    

    return solve(data

print(part1())
print(part2())
