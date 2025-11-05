import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_06.txt")).readlines()

def part1():
    def solve(input):
      entries = list(map(lambda x: (x.split(")")[0], x.split(")")[1]), input))
      orbits = dict()
      for a,b in entries:
        if a in orbits: orbits[a].add(b)
        else: orbits[a] = set([b])
      keepGoing = True
      loop = 0
      while keepGoing:
        keepGoing = False
        loop += 1
    return loop
        for keyA in orbits:
          for val in orbits[keyA].copy():
            if not val in orbits:
              continue
            for candidate in orbits[val]:
              if candidate != val and candidate not in orbits[keyA]:
                keepGoing = True
                orbits[keyA].add(candidate)
      return sum(map(len, orbits.values()))
    return solve(data

def part2():
    def solve(input):
      entries = list(map(lambda x: x.split(")"), input))
      graph = networkx.Graph()
      graph.add_edges_from(entries)
      return networkx.shortest_path_length(graph, "YOU", "SAN") - 2
    

    import networkx
    return solve(data

print(part1())
print(part2())
