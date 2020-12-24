from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import add
from itertools import chain, count, islice


@dataclass(frozen=True)
class Pos:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y, self.z + other.z)


ORIGIN = Pos(0, 0, 0)
NORTHEAST = Pos(1, -1, 0)
EAST = Pos(1, 0, -1)
SOUTHEAST = Pos(0, 1, -1)
SOUTHWEST = Pos(-1, 1, 0)
WEST = Pos(-1, 0, 1)
NORTHWEST = Pos(0, -1, 1)

DIRECTIONS = {
    "ne": NORTHEAST,
    "e": EAST,
    "se": SOUTHEAST,
    "sw": SOUTHWEST,
    "w": WEST,
    "nw": NORTHWEST,
}


def parse_directions(line):
    chars = iter(line)
    for c1 in chars:
        if (dir := DIRECTIONS.get(c1)) is not None:
            yield dir
            continue
        c2 = next(chars, None)
        if c2 is None:
            assert False
        yield DIRECTIONS[c1 + c2]


def parse(input):
    return map(parse_directions, input.splitlines())


def follow(coords):
    return reduce(add, coords, ORIGIN)


def tile(paths):
    room = defaultdict(lambda: False)
    for path in paths:
        pos = follow(path)
        room[pos] = not room[pos]
    return room


def black(room):
    return sum(room.values())


def part_1(input):
    print(black(tile(parse(input))))


def neighbors(pos):
    return (pos + dir for dir in DIRECTIONS.values())


def step(room):
    next = room.copy()
    tiles = {p for pos in room for p in chain(neighbors(pos), (pos,))}
    for tile in tiles:
        black = sum(room[pos] for pos in neighbors(tile))
        if room[tile]:
            if black == 0 or black > 2:
                next[tile] = False
        else:
            if black == 2:
                next[tile] = True
    return next


def iterate(fn, value):
    return (value := fn(value) for _ in count())


def nth(iter, n):
    return next(islice(iter, n - 1, n))


def part_2(input):
    print(black(nth(iterate(step, tile(parse(input))), 100)))
