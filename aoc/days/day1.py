from functools import reduce
from itertools import permutations
from operator import mul


def prod(iter):
    return reduce(mul, iter, 1)


def solve(input, n):
    return prod(
        next(v for v in permutations(map(int, input.splitlines()), n) if sum(v) == 2020)
    )


def part_1(input):
    print(solve(input, 2))


def part_2(input):
    print(solve(input, 3))
