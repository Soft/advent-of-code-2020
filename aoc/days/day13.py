from operator import itemgetter


def parse(input):
    time, lines = input.splitlines()
    return int(time), [int(line) for line in lines.split(",") if line != "x"]


def next_departure(time, line):
    departure = time // line * line
    if departure < time:
        departure += line
    return departure


def part_1(input):
    time, lines = parse(input)
    line, departure = min(
        ((line, next_departure(time, line)) for line in lines), key=itemgetter(1),
    )
    wait = departure - time
    print(line * wait)
