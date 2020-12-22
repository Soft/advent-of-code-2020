from collections import deque
from itertools import takewhile, count, starmap
from operator import mul


def identity(n):
    return n


def parse_deck(lines):
    next(lines)
    return deque(int(line) for line in takewhile(identity, lines))


def parse(input):
    lines = iter(input.splitlines())
    deck1 = parse_deck(lines)
    deck2 = parse_deck(lines)
    return deck1, deck2


def step(deck1, deck2):
    a = deck1.popleft()
    b = deck2.popleft()
    assert a != b
    if a > b:
        deck1.extend((a, b))
    else:
        deck2.extend((b, a))


def play(deck1, deck2):
    while deck1 and deck2:
        step(deck1, deck2)
    return deck1 or deck2


def part_1(input):
    winner = play(*parse(input))
    print(sum(starmap(mul, zip(winner, count(len(winner), -1)))))
