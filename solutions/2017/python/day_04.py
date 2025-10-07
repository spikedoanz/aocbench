data = [row.split() for row in open("inputs/2017_04.txt").readlines()]

print(sum(1 for p in data if len(p) == len(set(p))))
print(sum(1 for p in data if len(p) == len(set([tuple(sorted(w)) for w in p]))))
