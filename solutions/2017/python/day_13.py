import itertools
import os

INPUT_DIR = os.path.expanduser(os.getenv("AOC_INPUT_DIR", "~/.cache/aocb/inputs/"))
with open(os.path.join(INPUT_DIR, "2017_13.txt")) as f:
    scanners = {
        int(depth): int(rng)
        for depth, rng in (line.strip().split(": ") for line in f if line.strip())
    }

# Capture times when the packet gets caught given a start delay.
def caught_positions(delay: int) -> list[int]:
    return [
        depth * scanners[depth]
        for depth in scanners
        if (depth + delay) % (scanners[depth] * 2 - 2) == 0
    ]

print(sum(caught_positions(0)))
print(next(delay for delay in itertools.count(0) if not caught_positions(delay)))
