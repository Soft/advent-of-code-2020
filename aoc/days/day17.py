from collections import defaultdict
from itertools import product

OFFSETS = frozenset(off for off in product((-1, 0, 1), repeat=3))
NEIGHBOR_OFFSETS = frozenset(off for off in OFFSETS if off != (0, 0, 0))


def parse(input):
    world = defaultdict(lambda: False)
    for y, row in enumerate(input.splitlines()):
        for x, col in enumerate(row):
            if col == "#":
                world[(x, y, 0)] = True
    return world


def neighbors(x, y, z):
    yield from ((x + x1, y + y1, z + z1) for x1, y1, z1 in NEIGHBOR_OFFSETS)


def perimeter(x, y, z):
    yield from ((x + x1, y + y1, z + z1) for x1, y1, z1 in OFFSETS)


def step(world):
    next = world.copy()
    cells = {c for pos in world for c in perimeter(*pos)}
    for cell in cells:
        active_neighbors = sum(world[pos] for pos in neighbors(*cell))
        if world[cell]:
            if active_neighbors not in (2, 3):
                next[cell] = False
        else:
            if active_neighbors == 3:
                next[cell] = True
    return next


def simulate(world, steps=6):
    current = world
    for _ in range(steps):
        current = step(current)
    return current


def active(world):
    return sum(world[pos] for pos in world)


def part_1(input):
    world = parse(input)
    print(active(simulate(world)))
