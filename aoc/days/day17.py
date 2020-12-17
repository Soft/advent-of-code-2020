from collections import defaultdict
from functools import partial
from itertools import product, starmap
from operator import add

OFFSETS_3D = frozenset(product((-1, 0, 1), repeat=3))
OFFSETS_4D = frozenset(product((-1, 0, 1), repeat=4))


def pad(source, size):
    assert len(source) <= size
    dest = [0] * size
    dest[: len(source)] = source
    return tuple(dest)


def parse(input, dim=3):
    return defaultdict(
        lambda: False,
        (
            (pad((x, y), dim), True)
            for y, row in enumerate(input.splitlines())
            for x, col in enumerate(row)
            if col == "#"
        ),
    )


def perimeter(offsets, pos):
    return (tuple(starmap(add, zip(pos, off))) for off in offsets)


def neighbors(perimeter, pos):
    return (p for p in perimeter(pos) if p != pos)


def step(perimeter, world):
    next = world.copy()
    cells = {c for pos in world for c in perimeter(pos)}
    for cell in cells:
        active_neighbors = sum(world[pos] for pos in neighbors(perimeter, cell))
        if world[cell]:
            if active_neighbors not in (2, 3):
                next[cell] = False
        else:
            if active_neighbors == 3:
                next[cell] = True
    return next


def simulate(world, step, steps=6):
    current = world
    for _ in range(steps):
        current = step(current)
    return current


def active(world):
    return sum(world[pos] for pos in world)


def part_1(input):
    world = parse(input)
    perimeter_3d = partial(perimeter, OFFSETS_3D)
    step_3d = partial(step, perimeter_3d)
    print(active(simulate(world, step_3d)))


def part_2(input):
    world = parse(input, dim=4)
    perimeter_4d = partial(perimeter, OFFSETS_4D)
    step_4d = partial(step, perimeter_4d)
    print(active(simulate(world, step_4d)))
