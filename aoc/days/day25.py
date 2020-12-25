from itertools import count


def parse(input):
    pubk1, pubk2, *_ = input.splitlines()
    return int(pubk1), int(pubk2)


def loop_size(key):
    value = 1
    for size in count(1):
        value = value * 7 % 20201227
        if value == key:
            return size


def transform(sn, size):
    value = 1
    for _ in range(size):
        value = value * sn % 20201227
    return value


def part_1(input):
    pubk1, pubk2 = parse(input)
    print(transform(pubk1, loop_size(pubk2)))
