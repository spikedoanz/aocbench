import re

FIRST = 20151125
BASE = 252533
MOD = 33554393

data = open("inputs/2015_25.txt").read()
ROW, COL = map(int, re.findall(r'\d+', data))


def find_exp(r, c):
    return sum(range(r+c-1)) + c - 1

def solve(base, exp, mod):
    res = 1
    while exp:
        if exp % 2: res = res * base % mod
        exp //= 2
        base = base**2 % mod
    return res * FIRST % mod


print(solve(BASE, find_exp(ROW, COL), MOD))
