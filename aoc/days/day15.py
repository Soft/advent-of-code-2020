from itertools import count, islice


def record(map, num, turn):
    if num in map:
        prev = map[num][0]
        map[num] = (turn, prev)
    else:
        map[num] = (turn, None)


def generate(prelude):
    seen = {}
    for i, n in enumerate(prelude, 1):
        record(seen, n, i)
        prev = n
        yield prev
    for i in count(i + 1):
        if seen[prev][1] is None:
            prev = 0
            record(seen, 0, i)
        else:
            a, b = seen[prev]
            prev = a - b
            record(seen, prev, i)
        yield prev


def part_1(input):
    prelude = map(int, input.split(","))
    print(next(islice(generate(prelude), 2019, 2020)))


def part_2(input):
    prelude = map(int, input.split(","))
    print(next(islice(generate(prelude), 30000000 - 1, 30000000)))
