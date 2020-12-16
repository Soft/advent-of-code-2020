from itertools import takewhile
from dataclasses import dataclass
import re

FIELD_RE = re.compile(r"([^:]+): (\d+)-(\d+) or (\d+)-(\d+)")


@dataclass
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
    ticket = parse_tickets(lines)[0]
    nearby_tickets = parse_tickets(lines)
    return fields, ticket, nearby_tickets


def part_1(input):
    fields, _, tickets = parse(input)

    def valid_value(n):
        return any(n in a or n in b for a, b in fields.values())

    print(
        sum(
            sum(field for field in ticket if not valid_value(field))
            for ticket in tickets
        )
    )
