from collections import Counter


def jolts(input):
    jolts = sorted(int(n) for n in input.splitlines())
    jolts.insert(0, 0)
    jolts.append(jolts[-1] + 3)
    return jolts


def sliding_pairs(iterable):
    iterator = iter(iterable)
    prev = next(iterator)
    for item in iterator:
        yield prev, item
        prev = item


def part_1(input):
    differences = Counter(b - a for a, b in sliding_pairs(jolts(input)))
    print(differences[1] * differences[3])
