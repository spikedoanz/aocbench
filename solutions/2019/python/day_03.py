import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_03.txt")).readlines()

def part1():
    def lineToTupleSet(line):
        points = set()
        x = 0
        y = 0
        for instruction in line.split(","):
            direction = instruction[0]
            length = int(instruction[1:])
            for _ in range(0, length):
                if direction == "U": y -= 1
                if direction == "R": x += 1
                if direction == "D": y += 1
                if direction == "L": x -= 1
                points.add((x, y))
        return points
    
    def distance(p1, p2 = (0, 0)):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def solve(input):
        points1 = lineToTupleSet(input[0])
        points2 = lineToTupleSet(input[1])
        crossings = points1 & points2
        return min(map(distance, crossings))
    
    return solve(lines)

def part2():
    def lineToTupleDict(line):
        points = {}
        cost = 0
        x = 0
        y = 0
        for instruction in line.split(","):
            direction = instruction[0]
            length = int(instruction[1:])
            for _ in range(0, length):
                cost += 1
                if direction == "U": y -= 1
                if direction == "R": x += 1
                if direction == "D": y += 1
                if direction == "L": x -= 1
                if (x, y) not in points:
                    points[(x, y)] = cost
        return points
    
    def solve(input):
        points1 = lineToTupleDict(input[0])
        points2 = lineToTupleDict(input[1])
        crossings = set(points1.keys()) & set(points2.keys())
        return min(map(lambda p: points1[p] + points2[p], crossings))
    
    return solve(lines)

print(part1())
print(part2())