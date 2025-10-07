from collections import Counter

noise = open("inputs/2016_06.txt").readlines()

columns = (''.join(column) for column in zip(*noise))

first_solution = ''
second_solution = ''

for column in columns:
    (most, _), *others, (least, _) = Counter(column).most_common()
    first_solution += most
    second_solution += least

print(first_solution)
print(second_solution)
