from copy import deepcopy
from dataclasses import dataclass
from functools import partial
from itertools import count, product, takewhile
from typing import List


def takewhile1(pred, iterable):
    """
    variant of takewhile that also returns the first item where pred does not
    return True.
    """
    for item in iterable:
        ok = pred(item)
        yield item
        if not ok:
            break


@dataclass
class Room:
    layout: List[List[str]]
    width: int
    height: int

    @classmethod
    def parse(cls, input):
        layout = list(map(list, input.splitlines()))
        return cls(layout, len(layout[0]), len(layout))

    def tile(self, x, y):
        return self.layout[y][x]

    def set_tile(self, x, y, c):
        self.layout[y][x] = c

    def positions(self):
        return product(range(self.width), range(self.height))

    def neighbors(self, x, y):
        adjacent = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x, y + 1),
            (x - 1, y + 1),
            (x - 1, y),
        ]
        return filter(self.inside, adjacent)

    def visible(self, x, y):
        def floor(pos):
            x, y = pos
            return self.tile(x, y) == "."

        def visible_tiles(coords):
            return takewhile1(floor, takewhile(self.inside, coords))

        yield from visible_tiles((x - n, y - n) for n in count(1))
        yield from visible_tiles((x, y - n) for n in count(1))
        yield from visible_tiles((x + n, y - n) for n in count(1))
        yield from visible_tiles((x + n, y) for n in count(1))
        yield from visible_tiles((x + n, y + n) for n in count(1))
        yield from visible_tiles((x, y + n) for n in count(1))
        yield from visible_tiles((x - n, y + n) for n in count(1))
        yield from visible_tiles((x - n, y) for n in count(1))

    def inside(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def occupied_seats(self):
        return sum(self.tile(nx, ny) == "#" for nx, ny in self.positions())

    def occupied_neighbors(self, x, y):
        return sum(self.tile(nx, ny) == "#" for nx, ny in self.neighbors(x, y))

    def occupied_visible(self, x, y):
        return sum(self.tile(nx, ny) == "#" for nx, ny in self.visible(x, y))


def step(vacant, occupied, room):
    next = deepcopy(room)
    for x, y in room.positions():
        cell = room.tile(x, y)
        if cell == "L" and vacant(room, x, y):
            next.set_tile(x, y, "#")
        elif cell == "#" and occupied(room, x, y):
            next.set_tile(x, y, "L")
    return next


def until_stable(fn, input):
    prev = object()
    current = input
    while prev != current:
        prev = current
        current = fn(current)
    return current


def part_1(input):
    vacant = lambda room, x, y: room.occupied_neighbors(x, y) == 0
    occupied = lambda room, x, y: room.occupied_neighbors(x, y) >= 4
    stepper = partial(step, vacant, occupied)
    print(until_stable(stepper, Room.parse(input)).occupied_seats())


def part_2(input):
    vacant = lambda room, x, y: room.occupied_visible(x, y) == 0
    occupied = lambda room, x, y: room.occupied_visible(x, y) >= 5
    stepper = partial(step, vacant, occupied)
    print(until_stable(stepper, Room.parse(input)).occupied_seats())
