from collections import deque
from itertools import takewhile, count, starmap, islice
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


def step1(deck1, deck2):
    a = deck1.popleft()
    b = deck2.popleft()
    assert a != b
    if a > b:
        deck1.extend((a, b))
    else:
        deck2.extend((b, a))


def play1(deck1, deck2):
    while deck1 and deck2:
        step1(deck1, deck2)
    return deck1 or deck2


def score(deck):
    return sum(starmap(mul, zip(deck, count(len(deck), -1))))


def part_1(input):
    print(score(play1(*parse(input))))


def step2(deck1, deck2):
    a = deck1.popleft()
    b = deck2.popleft()
    assert a != b

    if len(deck1) >= a and len(deck2) >= b:
        deck1_ = deque(islice(deck1, a))
        deck2_ = deque(islice(deck2, b))
        winner = play2(deck1_, deck2_)
        if winner is deck1_:
            deck1.extend((a, b))
        elif winner is deck2_:
            deck2.extend((b, a))
        else:
            assert False
    else:
        if a > b:
            deck1.extend((a, b))
        else:
            deck2.extend((b, a))


def play2(deck1, deck2):
    past_decks1 = set()
    past_decks2 = set()
    while deck1 and deck2:
        key1 = tuple(deck1)
        key2 = tuple(deck2)
        if key1 in past_decks1 and key2 in past_decks2:
            return deck1
        past_decks1.add(key1)
        past_decks2.add(key2)
        step2(deck1, deck2)
    return deck1 or deck2


def part_2(input):
    print(score(play2(*parse(input))))
