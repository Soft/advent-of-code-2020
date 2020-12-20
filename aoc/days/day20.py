import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from itertools import takewhile
from operator import itemgetter, mul
from typing import Tuple

TITLE_RE = re.compile(r"Tile (\d+):")


@dataclass
class RawTile:
    id: int
    tile: Tuple[Tuple[str]]


@dataclass
class Tile:
    id: int
    top: Tuple[str]
    right: Tuple[str]
    bottom: Tuple[str]
    left: Tuple[str]


class Border(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()


def identity(n):
    return n


def parse_tile(lines):
    if (title := next(lines, None)) is None:
        return
    title = TITLE_RE.fullmatch(title)
    assert title is not None
    tile = tuple(map(tuple, takewhile(identity, lines)))
    return RawTile(int(title.group(1)), tile)


def parse(input):
    lines = iter(input.splitlines())
    while True:
        if (tile := parse_tile(lines)) is None:
            break
        yield tile


def column(tile, i):
    return tuple(map(itemgetter(i), tile))


def edges(tile):
    top = tile[0]
    right = column(tile, len(tile[0]) - 1)
    bottom = tile[len(tile) - 1]
    left = column(tile, 0)
    return top, right, bottom, left


def rotate_clockwise(tile):
    return tuple(map(flip_v, zip(*tile)))


def rotations(tile):
    yield tile
    yield (tile := rotate_clockwise(tile))
    yield (tile := rotate_clockwise(tile))
    yield (tile := rotate_clockwise(tile))


def flip_h(tile):
    return tuple(tuple(reversed(row)) for row in tile)


def flip_v(tile):
    return tuple(reversed(tile))


def flips(tile):
    yield tile
    yield flip_h(tile)
    yield flip_v(tile)
    yield flip_v(flip_h(tile))


def build_edge_dict(tiles):
    edgedict = defaultdict(list)
    for raw_tile in tiles:
        for rot in rotations(raw_tile.tile):
            for flip in flips(rot):
                top, right, bottom, left = edges(flip)
                tile = Tile(raw_tile.id, top, right, bottom, left)
                edgedict[(Border.TOP, top)].append(tile)
                edgedict[(Border.RIGHT, right)].append(tile)
                edgedict[(Border.BOTTOM, bottom)].append(tile)
                edgedict[(Border.LEFT, left)].append(tile)
    return edgedict


def construct(tiles):
    edgedict = build_edge_dict(tiles)
    used = set()
    placed = {}

    def find_tile(border, edge):
        return next(
            (tile for tile in edgedict[border, edge] if tile.id not in used),
            None,
        )

    def place_tile(tile, x, y):
        if tile.id in used:
            return
        used.add(tile.id)
        placed[(x, y)] = tile.id

        for border, edge in zip(
            Border, (tile.top, tile.right, tile.bottom, tile.left)
        ):
            if border is Border.TOP:
                if (tile := find_tile(Border.BOTTOM, edge)) is not None:
                    place_tile(tile, x, y - 1)
            elif border is Border.RIGHT:
                if (tile := find_tile(Border.LEFT, edge)) is not None:
                    place_tile(tile, x + 1, y)
            elif border is Border.BOTTOM:
                if (tile := find_tile(Border.TOP, edge)) is not None:
                    place_tile(tile, x, y + 1)
            elif border is Border.LEFT:
                if (tile := find_tile(Border.RIGHT, edge)) is not None:
                    place_tile(tile, x - 1, y)

    start = next(iter(edgedict.values()))[0]
    place_tile(start, 0, 0)
    return placed


def corners(placed):
    min_x, _ = min(placed, key=itemgetter(0))
    max_x, _ = max(placed, key=itemgetter(0))
    _, min_y = min(placed, key=itemgetter(1))
    _, max_y = max(placed, key=itemgetter(1))
    nw = placed[(min_x, min_y)]
    ne = placed[(max_x, min_y)]
    se = placed[(max_x, max_y)]
    sw = placed[(min_x, max_y)]
    return nw, ne, se, sw


def prod(iter):
    return reduce(mul, iter, 1)


def part_1(input):
    tiles = list(parse(input))
    print(prod(corners(construct(tiles))))
