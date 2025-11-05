import os
from collections import defaultdict
import re

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))

tasks = set()
deps = defaultdict(set)
for line in open(os.path.join(INPUT_DIR, "2018_07.txt")):
    a, b = re.findall(r' ([A-Z]) ', line)
    tasks |= {a, b}
    deps[b].add(a)

# part 1
done = []
for _ in tasks:
    done.append(min(x for x in tasks
        if x not in done and deps[x] <= set(done)))
print(''.join(done))

# part 2
done = set()
seconds = 0
counts = [0] * 5
work = [''] * 5
tasks_copy = tasks.copy()
while True:
    for i, count in enumerate(counts):
        if count == 1:
            done.add(work[i])
        counts[i] = max(0, count - 1)
    while 0 in counts:
        i = counts.index(0)
        candidates = [x for x in tasks_copy if deps[x] <= done]
        if not candidates:
            break
        task = min(candidates)
        tasks_copy.remove(task)
        counts[i] = ord(task) - ord('A') + 61
        work[i] = task
    if sum(counts) == 0:
        break
    seconds += 1
print(seconds)