import re
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from itertools import takewhile
from operator import mul

FIELD_RE = re.compile(r"([^:]+): (\d+)-(\d+) or (\d+)-(\d+)")
INTERESTING_FIELDS = frozenset(
    {
        "departure location",
        "departure station",
        "departure platform",
        "departure track",
        "departure date",
        "departure time",
    }
)


@dataclass(frozen=True)
class Range:
    min: int
    max: int

    def __contains__(self, n):
        return self.min <= n <= self.max


def identity(n):
    return n


def parse_fields(lines):
    def parse_field(line):
        field = FIELD_RE.fullmatch(line)
        assert field is not None
        return (
            field.group(1),
            (
                Range(int(field.group(2)), int(field.group(3))),
                Range(int(field.group(4)), int(field.group(5))),
            ),
        )

    return dict(parse_field(line) for line in takewhile(identity, lines))


def parse_tickets(lines):
    next(lines)  # skip header
    return list(tuple(map(int, line.split(","))) for line in takewhile(identity, lines))


def parse(input):
    lines = iter(input.splitlines())
    fields = parse_fields(lines)
    our_ticket = parse_tickets(lines)[0]
    nearby_tickets = parse_tickets(lines)
    return fields, our_ticket, nearby_tickets


def valid_value(fields, n):
    return any(n in a or n in b for a, b in fields)


def part_1(input):
    fields, _, tickets = parse(input)

    print(
        sum(
            sum(field for field in ticket if not valid_value(fields.values(), field))
            for ticket in tickets
        )
    )


def transpose(rows):
    return list(zip(*rows))


def column_fits(field, column):
    return all(c in field[0] or c in field[1] for c in column)


def candidates(fields, tickets):
    possible = defaultdict(set)
    for i, column in enumerate(transpose(tickets)):
        for name, field in fields.items():
            if column_fits(field, column):
                possible[name].add(i)
    return possible


def solve_fields(fields, tickets):
    possible_columns = candidates(fields, tickets)
    solved = {}
    while possible_columns:
        for field, possible in tuple(possible_columns.items()):
            if len(possible) == 1:
                col = next(iter(possible))
                solved[field] = col
                del possible_columns[field]
                for columns in possible_columns.values():
                    columns.discard(col)
    return solved


def prod(iter):
    return reduce(mul, iter, 1)


def part_2(input):
    fields, our_ticket, tickets = parse(input)

    valid_tickets = [
        ticket
        for ticket in tickets
        if all(valid_value(fields.values(), field) for field in ticket)
    ]

    solved = solve_fields(fields, valid_tickets)

    print(prod(our_ticket[solved[col]] for col in INTERESTING_FIELDS))
