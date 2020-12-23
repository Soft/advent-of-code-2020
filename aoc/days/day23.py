from __future__ import annotations
from itertools import cycle, islice
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: Node

    def __repr__(self):
        return "Node(value={}, next={})".format(
            self.value, self.next.value if self.next else None
        )


def parse(input):
    return [int(n) for n in input.rstrip()]


def sliding_pairs(iterable):
    iterator = iter(iterable)
    prev = next(iterator)
    for item in iterator:
        yield prev, item
        prev = item


def build_nodes(nums):
    nodes = {n: Node(n, None) for n in nums}
    for p, n in sliding_pairs(islice(cycle(nums), 0, len(nums) + 1)):
        nodes[p].next = nodes[n]
    return nodes


def step(min_label, max_label, cups, current):
    current_cup = cups[current]

    n1 = current_cup.next
    n2 = n1.next
    n3 = n2.next

    current_cup.next = n3.next

    destination = current
    while True:
        destination -= 1
        if destination < min_label:
            destination = max_label
        if destination in {n1.value, n2.value, n3.value}:
            continue
        break
    destination_cup = cups[destination]

    tmp = destination_cup.next
    destination_cup.next = n1
    n3.next = tmp

    return current_cup.next.value


def play(nodes, current, times):
    min_label = min(nodes)
    max_label = max(nodes)
    for _ in range(times):
        current = step(min_label, max_label, nodes, current)
    return nodes


def loop_around(nodes, n):
    start = nodes[n]
    current = start.next
    while current != start:
        yield current.value
        current = current.next


def part_1(input):
    nums = parse(input)
    nodes = play(build_nodes(nums), nums[0], 100)
    print("".join(map(str, loop_around(nodes, 1))))
