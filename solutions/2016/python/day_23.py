from math import factorial
import re

data = open("inputs/2016_23.txt").read()
# Extract the constants from lines like "cpy 98 c" and "jnz 86 d"
constants = re.findall(r'cpy (\d+)', data)
mult_const = int(constants[-2]) * int(constants[-1]) if len(constants) >= 2 else 87 * 70

def translate_asembunny(a):
    return factorial(a) + mult_const


print(translate_asembunny(a=7))
print(translate_asembunny(a=12))