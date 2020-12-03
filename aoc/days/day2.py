import re


def parse_line(line):
    match = re.match(r"^(\d+)\-(\d+) (.): (.+)$", line)
    return (
        int(match.group(1)),
        int(match.group(2)),
        match.group(3),
        match.group(4),
    )


def count_char(c, input):
    return sum(1 for a in input if a == c)


def is_valid_1(min, max, c, input):
    return min <= count_char(c, input) <= max


def is_valid_2(i, n, c, input):
    a = input[i - 1] == c
    b = input[n - 1] == c
    return a ^ b


def solve(input, validate):
    return sum(
        validate(*parsed)
        for parsed in (parse_line(line) for line in input.splitlines())
    )


def part_1(input):
    print(solve(input, is_valid_1))


def part_2(input):
    print(solve(input, is_valid_2))
