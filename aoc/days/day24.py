from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import add


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


def part_1(input):
    print(sum(tile(parse(input)).values()))
