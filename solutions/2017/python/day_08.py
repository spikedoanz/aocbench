ls = [x.strip().split() for x in open("inputs/2017_08.txt").readlines()]

o = {'==': 'eq', '!=': 'ne', '<=': 'le', '>=': 'ge', '<': 'lt', '>': 'gt'}
d, h = {}, 0

for w in ls:
    if getattr(d.get(w[4], 0), '__'+o[w[5]]+'__')(int(w[6])):
        d[w[0]] = d.get(w[0], 0) + (int(w[2]) if w[1] == 'inc' else -int(w[2]))
        h = max(h, d[w[0]])
print(max(d.values()))
print(h)
