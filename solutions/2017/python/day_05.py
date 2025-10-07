data = [int(row) for row in open("inputs/2017_05.txt").readlines()]

for c in (lambda _: False, lambda x: x > 2):
    m, s, i = list(data), 0, 0
    while 0 <= i < len(m):
        j = m[i]
        m[i] += -1 if c(j) else 1
        i += j
        s += 1
    print(s)
