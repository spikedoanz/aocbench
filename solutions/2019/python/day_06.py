import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

import networkx as nx


G = nx.read_edgelist('input', delimiter=')', create_using=nx.DiGraph)


def part1():
    return sum(len(nx.ancestors(G, v)) for v in G)


def part2():
    return nx.shortest_path_length(G.to_undirected(), 'YOU', 'SAN') - 2

print(part1())
print(part2())
