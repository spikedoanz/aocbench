import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
addresses = open(os.path.join(INPUT_DIR, "2016_20.txt")).read().split('\n')

ips = sorted([tuple(map(int, address.split('-'))) for address in addresses])


def find_lowest(ips):
    nr_available = 0
    lowest_available = 0
    the_lowest = 0

    for (low, high) in ips:
        if low > lowest_available:
            nr_available += low - lowest_available
            if not the_lowest:
                the_lowest = lowest_available
        lowest_available = max(lowest_available, high + 1)
    return the_lowest, nr_available


first, second = find_lowest(ips)

print(first)
print(second)
