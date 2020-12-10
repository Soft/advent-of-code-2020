from collections import Counter
from itertools import count
from functools import lru_cache


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


def neighbors(jolts, index):
    current = jolts[index]
    for i in count(index + 1):
        if i == len(jolts):
            return
        if jolts[i] - current <= 3:
            yield i
        else:
            return


def traverse_paths(jolts):
    @lru_cache(None)
    def traverse(index):
        if jolts[index] == jolts[-1]:
            return 1
        return sum(traverse(i) for i in neighbors(jolts, index))

    return traverse(0)


def part_2(input):
    print(traverse_paths(jolts(input)))
