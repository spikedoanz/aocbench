from math import factorial
import re

data = open("inputs/2016_23.txt").read()
# Extract the constants from lines like "cpy 98 c" and "jnz 86 d"
constants = re.findall(r'cpy (\d+)', data)
mult_const = int(constants[-2]) * int(constants[-1]) if len(constants) >= 2 else 87 * 70

def translate_asembunny(a):
    return factorial(a) + mult_const


print('Assembunny code again? Not a problem for me.')
print('If I start with 7 eggs in the register a, '
     f'I get {translate_asembunny(a=7)} as a final value for that register.')
print('....')
print('Oh! I should have started with 12 eggs in the register a!')
print(f'Then I get {translate_asembunny(a=12)} as a final value.')