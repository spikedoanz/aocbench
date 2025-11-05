import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_24.txt")).readlines()

def part1():
    def draw(level):
      size = 5 # assume a square
      for y in range(size):
        line = "".join([level[(x,y)] for x in range(size)])
    return line
    def stringify(level):
      return "".join(level.values())
    def neighbors(level, p):
      return [p for p in [
        (p[0] - 1, p[1]),
        (p[0] + 1, p[1]),
        (p[0], p[1] - 1),
        (p[0], p[1] + 1),
      ] if p in level]
    def solve(raw):
      level = dict()
      x,y = 0,0
      for line in raw:
        for c in line:
          level[(x,y)] = c
          x += 1
        y += 1
        x = 0
      layouts = set()
      while True:
        txt = stringify(level)
        if txt in layouts: break
        layouts.add(txt)
        newlevel = dict()
        for p in level:
          ns = neighbors(level, p)
          bugcount = sum([1 for n in ns if level[n] == "#"])
          if level[p] == "#" and not bugcount == 1: newlevel[p] = "."
          elif level[p] == "." and (bugcount == 1 or bugcount == 2): newlevel[p] = "#"
          else: newlevel[p] = level[p]
        level = newlevel
      power = 1
      result = 0
      for p in level:
        if level[p] == "#": result += power
        power = power * 2
      return result
    return "Solution:", solve(raw

def part2():
    def solve(raw):
      levels = dict()
      levels[0] = createlevel(raw)
      empty = createlevel([".....", ".....", "..?..", ".....", "....."])
      
      for minutes in range(200):
        print(f"At minute {minutes}")
        
        newlevels = dict()
    
        for depth in range(-minutes-1, minutes+2):
          if depth not in levels:
            levels[depth] = empty.copy()
    
          level = levels[depth]
          newlevel = dict()
          newlevels[depth] = newlevel
    
          for p in level:
            ns = neighbors(levels, depth, p)
            bugcount = sum([1 for n in ns if n == "#"])
            if level[p] == "#" and not bugcount == 1: newlevel[p] = "."
            elif level[p] == "." and (bugcount == 1 or bugcount == 2): newlevel[p] = "#"
            else: newlevel[p] = level[p]
    
        levels = newlevels
    
      # draw(levels)
    
      result = 0
      for rec in range(min(levels.keys()), max(levels.keys())):
        result += sum([1 for p in levels[rec] if levels[rec][p] == "#"])
    
      return result
    

    return "Solution:", solve(raw

print(part1())
print(part2())
