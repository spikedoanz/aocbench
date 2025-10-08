def compile_program(data):
    instructions = []
    for line in data:
        parts = line.split()
        op = parts[0]
        
        if op in ["hlf", "tpl", "inc"]:
            reg = 0 if parts[1].rstrip(',') == "a" else 1
            instructions.append((op, reg))
        elif op == "jmp":
            instructions.append((op, int(parts[1])))
        elif op in ["jie", "jio"]:
            reg = 0 if parts[1] == "a," else 1
            offset = int(parts[2])
            instructions.append((op, reg, offset))
    
    return instructions

def run_program_fast(a=0):
    b = 0
    regs = [a, b]
    ip = 0
    
    while ip < len(instructions):
        inst = instructions[ip]
        op = inst[0]
        
        if op == "hlf":
            regs[inst[1]] //= 2
        elif op == "tpl":
            regs[inst[1]] *= 3
        elif op == "inc":
            regs[inst[1]] += 1
        elif op == "jmp":
            ip += inst[1] - 1
        elif op == "jie":
            if regs[inst[1]] % 2 == 0:
                ip += inst[2] - 1
        elif op == "jio":
            if regs[inst[1]] == 1:
                ip += inst[2] - 1
        ip += 1
    
    return regs[1]

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', 'inputs'))
data = open(os.path.join(INPUT_DIR, "2015_23.txt")).read().splitlines()
instructions = compile_program(data)
print(run_program_fast(0))
print(run_program_fast(1))
