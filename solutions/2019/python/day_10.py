import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_10.txt")).readlines()

def part1():
    import math
    def solve(input):
      points = dict()
      x, y = -1, -1
      for line in input:
        y += 1
        x = -1
        for char in line:
          x += 1
          if char == "#":
            points[(x,y)] = dict()
      for p in points.keys():
        for other in points.keys():
          if p == other: continue
          rad = math.atan2(other[1]-p[1], other[0]-p[0])
          key = int(rad * 100000) + 1
          if key not in points[p]:
            points[p][key] = list()
          points[p][key].append(other)
        #print(p, points[p], len(points[p]))
      result = max(points, key = lambda p: len(points[p].values()))
      return result, ' visible: ', len(points[result].values())
    return solve(data

def part2():
    def solve(input):
      points = dict()
      x, y = -1, -1
    
      for line in input:
        y += 1
        x = -1
        for char in line:
          x += 1
          if char == "#":
            points[(x,y)] = dict()
      
      for p in points.keys():
        for other in points.keys():
          if p == other: continue
          rad = math.atan2(other[1]-p[1], other[0]-p[0])
          if rad < (math.pi / 2 * -1): rad = math.pi + math.pi + rad
          key = int(rad * 1000000)
          if key not in points[p]:
            points[p][key] = list()
          points[p][key].append(other)
        
      station = max(points, key = lambda p: len(points[p].values()))
    
      for p in points.keys():
        for key in points[p].keys():
          points[p][key].sort(key = lambda p2: abs(p[0] - p2[0]) + abs(p[1] - p2[1]))
    
      print('station at', station)
      for x in sorted(points[station].keys()): print(x, ' => ', points[station][x])
    
      i = 0
      printed = True
      while i < 200 and printed:
        printed = False
        for key in sorted(points[station].keys()):
          if len(points[station][key]) == 0: continue
          i += 1
          target = points[station][key].pop(0)
          result = target[0] * 100 + target[1]
          print(i, 'zapping', target, 'result would be', result)
          printed = True
          if i == 200: break
    
      return 'done for station', station
    

    import math
    # Not 315
    return solve(data

print(part1())
print(part2())
