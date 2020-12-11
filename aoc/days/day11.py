from itertools import product
from collections import namedtuple
from copy import deepcopy


class Room(namedtuple("Room", ("layout", "width", "height"))):
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
        return ((x, y) for x, y in adjacent if self.inside(x, y))

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


def occupied(room):
    return sum(room.tile(nx, ny) == "#" for nx, ny in room.positions())


def occupied_neighbors(room, x, y):
    return sum(room.tile(nx, ny) == "#" for nx, ny in room.neighbors(x, y))


def step(room):
    next = deepcopy(room)
    for x, y in room.positions():
        cell = room.tile(x, y)
        if cell == "L" and occupied_neighbors(room, x, y) == 0:
            next.set_tile(x, y, "#")
        elif cell == "#" and occupied_neighbors(room, x, y) >= 4:
            next.set_tile(x, y, "L")
    return next


def part_1(input):
    prev = None
    state = Room.parse(input)
    while prev != state:
        prev = state
        state = step(state)
    print(occupied(state))
