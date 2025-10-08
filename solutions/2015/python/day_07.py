from functools import lru_cache
from operator import and_, or_, lshift, rshift


parse_input = lambda data: {(s := line.split(' -> '))[1]: s[0].split() for line in data}

def get_value(wires, wire='a', b=None):
    operations = {'AND': and_, 'OR': or_, 'LSHIFT': lshift, 'RSHIFT': rshift}
    @lru_cache
    def aux(wire):
        try: return int(wire)
        except ValueError: lhs = wires[wire]
        return ( aux(lhs[0])          if len(lhs) == 1 else
                ~aux(lhs[1]) & 0xffff if len(lhs) == 2 else
                operations[lhs[1]](aux(lhs[0]), aux(lhs[2])))
    if b is not None: wires['b'] = [b]
    return aux(wire)


import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = open(os.path.join(INPUT_DIR, "2015_07.txt")).read().splitlines()
wires = parse_input(data)

print(first := get_value(wires))
print(get_value(wires, b=first))