from hashlib import md5

import os

INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
SALT = open(os.path.join(INPUT_DIR, "2016_14.txt")).read().strip()


def find_keys(second_part=False):
    triplets = {}
    valid_keys = set()
    index = 0

    while len(valid_keys) < 64 or index < max(valid_keys) + 1000:
        hex_ = md5((SALT+str(index)).encode()).hexdigest()

        if second_part:
            for _ in range(2016):
                hex_ = md5(hex_.encode()).hexdigest()

        found_triplet = False
        for a, b, c in zip(hex_, hex_[1:], hex_[2:]):
            if a == b == c:
                if 5*a in hex_:
                    for k, v in triplets.items():
                        if a == v and k < index <= 1000+k:
                            valid_keys.add(k)
                if not found_triplet:
                    triplets[index] = a
                    found_triplet = True
        index += 1
    return sorted(valid_keys)[63]


print(find_keys())
print(find_keys('second'))
