import argparse
import functools
import pkgutil
import re
import sys
from importlib import resources
from pathlib import Path

import aoc.days
import aoc.input


class Solution:
    def __init__(self, module_info):
        self._module_info = module_info
        self._module = None

    @property
    def day(self):
        return int(re.match(r"^day(\d+)$", self._module_info.name).group(1))

    def part(self, i):
        try:
            fn = getattr(self.module, f"part_{i}")
            return make_part(self.day, fn)
        except AttributeError:
            pass

    @property
    def module(self):
        if self._module is not None:
            return self._module
        self._module = self._module_info.module_finder.find_spec(
            self._module_info.name
        ).loader.load_module()
        return self._module


def make_part(day, fn):
    @functools.wraps(fn)
    def wrap(path=None):
        if path is None:
            input = resources.read_text(aoc.input, f"day{day}.txt")
        else:
            input = path.read_text()
        return fn(input)

    return wrap


def get_solutions():
    for module_info in pkgutil.iter_modules(aoc.days.__path__):
        yield Solution(module_info)


def fatal(message):
    prog = Path(sys.argv[0]).name
    print(f"{prog}: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("part", type=int)
    parser.add_argument("input", type=Path, nargs="?")
    args = parser.parse_args()

    solution = next(
        (solution for solution in get_solutions() if solution.day == args.day), None,
    )
    if solution is None:
        fatal("solution not available")
    part = solution.part(args.part)
    if part is None:
        fatal("part not available")
    part(args.input)
