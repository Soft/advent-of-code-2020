import re
from dataclasses import dataclass

MASK_RE = re.compile(r"mask = ([01X]+)")
STORE_RE = re.compile(r"mem\[(\d+)\] = (\d+)")


@dataclass
class Store:
    address: int
    value: int


@dataclass
class Mask:
    and_mask: str
    or_mask: str


def parse_mask(value):
    and_mask = int(re.sub("[X1]", "1", value), 2)
    or_mask = int(re.sub("[X0]", "0", value), 2)
    return Mask(and_mask, or_mask)


def instructions(input):
    for line in input.splitlines():
        mask = MASK_RE.fullmatch(line)
        if mask is not None:
            yield parse_mask(mask.group(1))
            continue
        store = STORE_RE.fullmatch(line)
        if store is not None:
            yield Store(int(store.group(1)), int(store.group(2)))
            continue
        assert False


def evaluate(instructions):
    mem = {}
    mask = None
    for instruction in instructions:
        if isinstance(instruction, Mask):
            mask = instruction
        elif isinstance(instruction, Store):
            value = instruction.value
            value &= mask.and_mask
            value |= mask.or_mask
            mem[instruction.address] = value
        else:
            assert False
    return mem


def part_1(input):
    print(sum(evaluate(instructions(input)).values()))
