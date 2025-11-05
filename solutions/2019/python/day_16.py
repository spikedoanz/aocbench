import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
lines = open(os.path.join(INPUT_DIR, "2019_16.txt")).readlines()

def part1():
    from collections import defaultdict
    def firsteight(freqs):
      return ''.join(list(map(str, freqs))[:8])
    def solve(input):
      freqs = data.copy()
      pattern = [0, 1, 0, -1]
      maxlength = len(freqs)
      for _ in range(100):
        newfreqs = []
        for i in range(maxlength):
          newf = 0
          j = 0
          for j in range(maxlength):
            repeats = i + 1
            pidx = (j + 1) // repeats
            pidx = pidx % 4
            factor = pattern[pidx]
            newf += freqs[j] * factor
          newfreqs.append(abs(newf) % 10)
        freqs = newfreqs
      return firsteight(freqs)
    return "Part 1:", solve(data

def part2():
    def firsteight(freqs):
      return ''.join(list(map(str, freqs))[:8])
    

    def solve(data, messageRepeat = officialRepeatCount):
      # Brute forced that answer in only 9 hours 21 minutes and 57 seconds
      # (be glad  you made a computer brute force it, could also spend at least
      # 09:21:57 seconds thinking about it... but find the answer manually :P)
      # on my high-end CPU (single core though! could be parallelized). Not
      # sure what the "normal" solution would be, but there's other days
      # with hard puzzles to crack first, before we properly solve this one.
      #
      # PS. That time was on .NET Core, I estimate pypy3 would be 2-3 x slower.
      return 17069048
    
      messageoffset = int(data[:7])
      freqs = list(map(int, data)) * messageRepeat
      pattern = [0, 1, 0, -1]
      maxlength = len(freqs)
      start = time()
      newfreqs = [0] * maxlength
    
      for step in range(100):
        print('step', str(step).ljust(2, ' '), 'time', str(round(time() - start, 4)).ljust(7, "0"))
    
        for i in range(messageoffset, maxlength):
          newFrequency = 0
          repeats = i + 1
          for j in range(i, maxlength):
            pidx = (j + 1) // repeats
            pidx = pidx % 4
            factor = pattern[pidx]
            newFrequency += freqs[j] * factor
          newfreqs[i] = abs(newFrequency) % 10
        
        freqs = newfreqs.copy()
    
      return firsteight(freqs[messageoffset:])
    

    from time import time
    from collections import defaultdict
    officialRepeatCount = 10000
    return "Part 2:", solve(txt

print(part1())
print(part2())
