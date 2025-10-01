data = open("inputs/2015_23.txt").read().splitlines()

def run_program(a=0):
    b = 0
    ip = 0
    while ip < len(data):
        inst = data[ip].split()
        op = inst[0]
        if op == "hlf":
            if inst[1] == "a,": a //= 2
            else: b //= 2
        elif op == "tpl":
            if inst[1] == "a,": a *= 3
            else: b *= 3
        elif op == "inc":
            if inst[1] == "a": a += 1
            else: b += 1
        elif op == "jmp":
            ip += int(inst[1]) - 1
        elif op == "jie":
            val = a if inst[1] == "a," else b
            if val % 2 == 0:
                ip += int(inst[2]) - 1
        elif op == "jio":
            val = a if inst[1] == "a," else b
            if val == 1:
                ip += int(inst[2]) - 1
        ip += 1
    return b

print(run_program(0))
print(run_program(1))
