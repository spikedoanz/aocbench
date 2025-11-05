from __future__ import annotations
import os
from dataclasses import dataclass

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
ns = list(map(int, open(os.path.join(INPUT_DIR, "2022_20.txt")).read().strip().split("\n")))


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def solve(part1):
    nodes = [Node(n) for n in ns]
    zero_node = next(node for node in nodes if node.value == 0)
    N = len(ns)

    for i in range(len(ns)):
        nodes[i].right = nodes[(i + 1) % N]
        nodes[i].left = nodes[(i - 1) % N]

    if not part1:
        for n in nodes:
            n.value *= 811589153

    for _ in range(1 if part1 else 10):
        for node in nodes:
            for _ in range(node.value % (N - 1)):
                a, b, c = node.left, node.right, node.right.right
                a.right = b
                b.left = a
                b.right = node
                node.left = b
                node.right = c
                c.left = node

    s = 0
    target = zero_node
    for _ in range(3):
        for _ in range(1000):
            target = target.right
        s += target.value
    return s


# Part 1
print(solve(True))

# Part 2
print(solve(False))
