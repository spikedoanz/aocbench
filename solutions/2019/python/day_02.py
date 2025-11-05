import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_02.txt")).readlines()

def part1():
    def solve(program):
      program[1] = 12
      program[2] = 2
      i = 0
      while True:
        if program[i] == 1:
          program[program[i+3]] = program[program[i+2]] + program[program[i+1]]
          i += 4
        elif program[i] == 2:
          program[program[i+3]] = program[program[i+2]] * program[program[i+1]]
          i += 4
        elif program[i] == 99:
          return program[0]
    return solve(data

def part2():
    def solve(input):
    
      for noun in range(0, 100):
        for verb in range(0, 100):
          program = input.copy()
    
          program[1] = noun
          program[2] = verb
    
          i = 0
    
          while True:
            if program[i] == 1:
              program[program[i+3]] = program[program[i+2]] + program[program[i+1]]
              i += 4
            elif program[i] == 2:
              program[program[i+3]] = program[program[i+2]] * program[program[i+1]]
              i += 4
            elif program[i] == 99:
              break
          
          if program[0] == 19690720:
            return 100 * noun + verb
    

    return solve(data

print(part1())
print(part2())
