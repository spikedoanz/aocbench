import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
d = [tuple(int(y) for y in x.strip().split('/')) for x in open(os.path.join(INPUT_DIR, "2017_24.txt")).readlines()]


def build(start, rem, maxlen=0, score=0):
    best = []
    for left, right in rem:
        if start in (left, right):
            subrem = rem[:]
            subrem.remove((left, right))
            myscore = score + left + right
            x = right if left == start else left
            cand = [(myscore, left, right)] + build(x, subrem, maxlen, myscore)
            best = cand if not best or (maxlen and len(cand) > len(best)) \
                or cand[-1] > best[-1] else best
    return best


print(build(0, d)[-1][0])
print(build(0, d, 1)[-1][0])
