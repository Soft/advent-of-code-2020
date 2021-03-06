import re
from dataclasses import dataclass
from itertools import product

MASK_RE = re.compile(r"mask = ([01X]+)")
STORE_RE = re.compile(r"mem\[(\d+)\] = (\d+)")
MAX_ADDRESS = 2 ** 36 - 1


@dataclass
class Store:
    address: int
    value: int


@dataclass
class Mask:
    value: str


def instructions(input):
    for line in input.splitlines():
        mask = MASK_RE.fullmatch(line)
        if mask is not None:
            yield Mask(mask.group(1))
            continue
        store = STORE_RE.fullmatch(line)
        if store is not None:
            yield Store(int(store.group(1)), int(store.group(2)))
            continue
        assert False


def evaluate1(instructions):
    mem = {}
    for instruction in instructions:
        if isinstance(instruction, Mask):
            and_mask = int(instruction.value.replace("X", "1"), 2)
            or_mask = int(instruction.value.replace("X", "0"), 2)
        elif isinstance(instruction, Store):
            mem[instruction.address] = instruction.value & and_mask | or_mask
        else:
            assert False
    return mem


def part_1(input):
    print(sum(evaluate1(instructions(input)).values()))


def expand_floating_masks(mask):
    indices = tuple(ind for ind, b in enumerate(reversed(mask)) if b == "X")
    for seq in product((True, False), repeat=len(indices)):
        and_mask = MAX_ADDRESS
        or_mask = 0
        for i, b in zip(indices, seq):
            if b:
                or_mask |= 1 << i
            else:
                and_mask &= ~(1 << i)
        yield and_mask, or_mask


def decode_address(mask, address):
    address |= int(mask.replace("X", "0"), 2)
    for and_mask, or_mask in expand_floating_masks(mask):
        yield address & and_mask | or_mask


def evaluate2(instructions):
    mem = {}
    for instruction in instructions:
        if isinstance(instruction, Mask):
            mask = instruction.value
        elif isinstance(instruction, Store):
            for address in decode_address(mask, instruction.address):
                mem[address] = instruction.value
        else:
            assert False
    return mem


def part_2(input):
    print(sum(evaluate2(instructions(input)).values()))
