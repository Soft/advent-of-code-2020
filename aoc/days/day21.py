import re
from collections import Counter
from itertools import chain

ENTRY_RE = re.compile(r"(.+) \(contains (.+)\)")


def parse(input):
    for line in input.splitlines():
        if (match := ENTRY_RE.fullmatch(line)) is not None:
            ingredients = frozenset(match.group(1).split(" "))
            allergens = frozenset(match.group(2).split(", "))
            yield ingredients, allergens
        else:
            assert False


def candidates(entries):
    result = {}
    for ingredients, allergens in entries:
        for allergen in allergens:
            if allergen in result:
                result[allergen] &= ingredients
            else:
                result[allergen] = set(ingredients)
    return result


def occurences(entries):
    return Counter(chain(*(ingredients for ingredients, _ in entries)))


def part_1(input):
    entries = list(parse(input))
    allergens = set(chain(*candidates(entries).values()))
    print(sum(v for k, v in occurences(entries).items() if k not in allergens))
