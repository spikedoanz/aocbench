import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

def parse_instruction(line):
    """Parse a single instruction line into components."""
    parts = line.strip().split()
    if len(parts) == 2:
        return (parts[0], parts[1], None)
    elif len(parts) == 3:
        return (parts[0], parts[1], parts[2])
    return None

def get_value(arg, registers):
    """Get the value of an argument (either a register or an integer)."""
    if arg in registers:
        return registers[arg]
    return int(arg)

def toggle_instruction(instruction):
    """Toggle an instruction according to the rules."""
    op = instruction[0]
    
    # For one-argument instructions
    if instruction[2] is None:
        if op == 'inc':
            return ('dec', instruction[1], None)
        else:  # dec or tgl
            return ('inc', instruction[1], None)
    
    # For two-argument instructions
    if op == 'jnz':
        return ('cpy', instruction[1], instruction[2])
    else:  # cpy or any other two-arg instruction
        return ('jnz', instruction[1], instruction[2])

def detect_multiplication_pattern(program, ip):
    """
    Detect common multiplication pattern in assembunny:
    cpy b c
    inc a
    dec c
    jnz c -2
    dec d
    jnz d -5
    
    This effectively does: a += b * d, then sets c=0 and d=0
    """
    if ip + 5 >= len(program):
        return None
    
    # Check for the multiplication pattern
    try:
        # Pattern varies, but common forms include:
        # Type 1: inc/dec loops
        if (program[ip][0] == 'cpy' and 
            program[ip+1][0] == 'inc' and
            program[ip+2][0] == 'dec' and
            program[ip+3][0] == 'jnz' and program[ip+3][2] == '-2' and
            program[ip+4][0] == 'dec' and
            program[ip+5][0] == 'jnz' and program[ip+5][2] == '-5'):
            
            # Found multiplication pattern
            src_reg = program[ip][1]  # Source register (b in example)
            tmp_reg = program[ip][2]  # Temp register (c in example)
            tgt_reg = program[ip+1][1]  # Target register (a in example)
            out_reg = program[ip+4][1]  # Outer loop register (d in example)
            
            return {
                'type': 'multiply',
                'source': src_reg,
                'temp': tmp_reg,
                'target': tgt_reg,
                'outer': out_reg,
                'length': 6
            }
    except:
        pass
    
    return None

def run_assembunny_optimized(instructions, initial_a=0):
    """Run the assembunny program with optimizations for common patterns."""
    # Initialize registers
    registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    
    # Parse all instructions
    program = [parse_instruction(line) for line in instructions if line.strip()]
    
    # Instruction pointer
    ip = 0
    
    # Track execution for optimization
    exec_count = 0
    max_exec = 10000000  # Safety limit
    
    # Execute instructions
    while 0 <= ip < len(program):
        exec_count += 1
        if exec_count > max_exec:
            print(f"Warning: Execution limit reached at ip={ip}")
            break
            
        if program[ip] is None:
            ip += 1
            continue
        
        # Check for multiplication pattern optimization
        mult_pattern = detect_multiplication_pattern(program, ip)
        if mult_pattern and mult_pattern['type'] == 'multiply':
            # Get register values
            src_val = get_value(mult_pattern['source'], registers)
            out_val = get_value(mult_pattern['outer'], registers)
            
            # Perform optimized multiplication
            registers[mult_pattern['target']] += src_val * out_val
            registers[mult_pattern['temp']] = 0
            registers[mult_pattern['outer']] = 0
            
            # Skip the multiplication loop
            ip += mult_pattern['length']
            continue
            
        op, arg1, arg2 = program[ip]
        
        if op == 'cpy':
            # Copy value to register (skip if target is not a register)
            if arg2 in registers:
                registers[arg2] = get_value(arg1, registers)
        
        elif op == 'inc':
            # Increment register
            if arg1 in registers:
                registers[arg1] += 1
        
        elif op == 'dec':
            # Decrement register
            if arg1 in registers:
                registers[arg1] -= 1
        
        elif op == 'jnz':
            # Jump if not zero
            if get_value(arg1, registers) != 0:
                ip += get_value(arg2, registers)
                continue
        
        elif op == 'tgl':
            # Toggle instruction at offset
            target = ip + get_value(arg1, registers)
            if 0 <= target < len(program) and program[target] is not None:
                program[target] = toggle_instruction(program[target])
        
        ip += 1
    
    return registers['a']

# Read the input
data = open(os.path.join(INPUT_DIR, "2016_23.txt")).read()
instructions = data.strip().split('\n')

# Part 1: Run with a=7
print(run_assembunny_optimized(instructions, initial_a=7))

# Part 2: Run with a=12 (should be much faster now!)
print(run_assembunny_optimized(instructions, initial_a=12))
