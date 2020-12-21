import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from itertools import takewhile, count, chain
from operator import itemgetter, mul
from typing import Tuple

TITLE_RE = re.compile(r"Tile (\d+):")
SEA_MONSTER = (
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
)


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
    tile: Tuple[Tuple[str]]


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
                tile = Tile(raw_tile.id, top, right, bottom, left, flip)
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
            (tile for tile in edgedict[border, edge] if tile.id not in used), None,
        )

    def place_tile(tile, x, y):
        if tile.id in used:
            return
        used.add(tile.id)
        placed[(x, y)] = tile

        for border, edge in zip(Border, (tile.top, tile.right, tile.bottom, tile.left)):
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


def bounds(placed):
    min_x, _ = min(placed, key=itemgetter(0))
    max_x, _ = max(placed, key=itemgetter(0))
    _, min_y = min(placed, key=itemgetter(1))
    _, max_y = max(placed, key=itemgetter(1))
    return min_x, min_y, max_x, max_y


def corners(placed):
    min_x, min_y, max_x, max_y = bounds(placed)
    nw = placed[(min_x, min_y)]
    ne = placed[(max_x, min_y)]
    se = placed[(max_x, max_y)]
    sw = placed[(min_x, max_y)]
    return nw, ne, se, sw


def prod(iter):
    return reduce(mul, iter, 1)


def part_1(input):
    print(prod(tile.id for tile in corners(construct(parse(input)))))


def trim(tile):
    return tuple(row[1:-1] for row in tile[1:-1])


def reorder(tiles):
    min_x, min_y, max_x, max_y = bounds(tiles)
    return (
        (tiles[(x, y)] for x in takewhile(lambda n: n <= max_x, count(min_x)))
        for y in takewhile(lambda n: n <= max_y, count(min_y))
    )


def merge(tiles):
    return tuple(tuple(chain(*row)) for tile_row in tiles for row in zip(*tile_row))


def hash_count(tile):
    return sum(col == "#" for row in tile for col in row)


def sliding_windows(n, lst):
    for i in range(0, len(lst) - n + 1):
        yield lst[i : i + n]


def fuzzy_match(pattern, string):
    assert len(pattern) == len(string)
    for p, c in zip(pattern, string):
        if p == "#":
            if c != "#":
                return False
    return True


def multiline_match_count(pattern, lines):
    matches = 0
    if len(lines) < len(pattern):
        return matches
    first, *others = pattern
    pattern_len = len(first)
    for x, piece in enumerate(sliding_windows(pattern_len, lines[0])):
        if fuzzy_match(first, piece):
            for pattern, line in zip(others, lines[1:]):
                if not fuzzy_match(pattern, line[x : x + pattern_len]):
                    break
            else:
                matches += 1
    return matches


def pattern_count(pattern, tile):
    return sum(multiline_match_count(pattern, tile[row:]) for row in range(len(tile)))


def find_patterns(pattern, image):
    for rot in rotations(image):
        for flip in flips(rot):
            if (matches := pattern_count(pattern, flip)) > 0:
                return matches
    return 0


def part_2(input):
    positions = construct(parse(input))
    image = merge(
        (trim(tile.tile) for tile in tile_row) for tile_row in reorder(positions)
    )
    total_hashes = hash_count(image)
    monster_hashes = hash_count(SEA_MONSTER)
    monster_count = find_patterns(SEA_MONSTER, image)
    print(total_hashes - monster_count * monster_hashes)
