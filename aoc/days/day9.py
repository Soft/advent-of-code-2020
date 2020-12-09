from itertools import combinations


def numbers(input):
    return [int(n) for n in input.splitlines()]


def find_invalid(sequence):
    for i, num in enumerate(sequence[25:], 25):
        if num not in {a + b for a, b in combinations(sequence[i - 25 : i], 2)}:
            return num


def part_1(input):
    print(find_invalid(numbers(input)))


def find_weakness(sequence):
    invalid = find_invalid(sequence)
    for i, n in enumerate(sequence):
        acc = n
        min_ = n
        max_ = n
        for x in sequence[i + 1 :]:
            acc += x
            min_ = min(x, min_)
            max_ = max(x, max_)
            if acc > invalid:
                break
            if acc == invalid:
                return min_ + max_


def part_2(input):
    print(find_weakness(numbers(input)))
