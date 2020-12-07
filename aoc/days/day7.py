import re
from functools import lru_cache

RELATION_RE = re.compile(r"(.+) bags contain (.+)\.")
ITEM_RE = re.compile(r"(\d+) (.+) bags?")


def bags(input):
    """Bags and their contents"""
    results = {}
    for line in input.splitlines():
        match = RELATION_RE.fullmatch(line)
        assert match is not None
        bag = match.group(1)
        items = match.group(2)
        contents = {}
        if items != "no other bags":
            for item in items.split(", "):
                match = ITEM_RE.fullmatch(item)
                assert match is not None
                contents[match.group(2)] = int(match.group(1))
        results[bag] = contents
    return results


def reverse_bags(bags):
    """Which bags can contain a particular bag"""
    results = {}
    for outer_bag, items in bags.items():
        for inner_bag, count in items.items():
            if inner_bag not in results:
                results[inner_bag] = {}
            results[inner_bag][outer_bag] = count
    return results


def outer_bags(bags, root):
    contained_in = reverse_bags(bags)
    bags = set()

    def traverse(bag):
        for outer_bag in contained_in.get(bag, {}):
            bags.add(outer_bag)
            traverse(outer_bag)

    traverse(root)
    return bags


def part_1(input):
    print(len(outer_bags(bags(input), "shiny gold")))


def inner_bag_count(bags, root):
    @lru_cache(None)
    def traverse(bag):
        total = 0
        for inner_bag, count in bags.get(bag, {}).items():
            total += count
            for _ in range(count):
                total += traverse(inner_bag)
        return total

    return traverse(root)


def part_2(input):
    print(inner_bag_count(bags(input), "shiny gold"))
