from collections import defaultdict
from itertools import product, starmap
from operator import add

OFFSETS_3D = frozenset(off for off in product((-1, 0, 1), repeat=3))
OFFSETS_4D = frozenset(off for off in product((-1, 0, 1), repeat=4))


def pad(source, size):
    assert len(source) <= size
    dest = [0] * size
    dest[: len(source)] = source
    return tuple(dest)


def parse(input, dim=3):
    world = defaultdict(lambda: False)
    for y, row in enumerate(input.splitlines()):
        for x, col in enumerate(row):
            if col == "#":
                world[pad((x, y), dim)] = True
    return world


def perimeter(pos, *, offsets=OFFSETS_3D):
    yield from (tuple(starmap(add, zip(pos, off))) for off in offsets)


def neighbors(pos, *, offsets=OFFSETS_3D):
    yield from (p for p in perimeter(pos, offsets=offsets) if p != pos)


def step(world, offsets=OFFSETS_3D):
    next = world.copy()
    cells = {c for pos in world for c in perimeter(pos, offsets=offsets)}
    for cell in cells:
        active_neighbors = sum(world[pos] for pos in neighbors(cell, offsets=offsets))
        if world[cell]:
            if active_neighbors not in (2, 3):
                next[cell] = False
        else:
            if active_neighbors == 3:
                next[cell] = True
    return next


def simulate(world, offsets=OFFSETS_3D, steps=6):
    current = world
    for _ in range(steps):
        current = step(current, offsets=offsets)
    return current


def active(world):
    return sum(world[pos] for pos in world)


def part_1(input):
    world = parse(input)
    print(active(simulate(world)))


def part_2(input):
    world = parse(input, dim=4)
    print(active(simulate(world, OFFSETS_4D)))
