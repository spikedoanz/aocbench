import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
d = [tuple(int(y) for y in x.strip().split('/')) for x in open(os.path.join(INPUT_DIR, "2017_24.txt")).readlines()]


def build(start, rem, part2=False):
    best = (0, 0)  # (length, strength)
    for left, right in rem:
        if start in (left, right):
            subrem = rem[:]
            subrem.remove((left, right))
            x = right if left == start else left
            sub_len, sub_str = build(x, subrem, part2)
            total_len = sub_len + 1
            total_str = sub_str + left + right
            if part2:
                if total_len > best[0] or (total_len == best[0] and total_str > best[1]):
                    best = (total_len, total_str)
            else:
                if total_str > best[1]:
                    best = (total_len, total_str)
    return best


print(build(0, d, False)[1])
print(build(0, d, True)[1])
