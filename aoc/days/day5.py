def lower_half(start, end):
    assert start < end
    offset = (end - start) // 2
    return start, start + offset


def upper_half(start, end):
    assert start < end
    offset = (end - start) // 2
    return start + offset + 1, end


def traverse(input, lower, upper, start, end):
    for c in input:
        if c == lower:
            start, end = lower_half(start, end)
        elif c == upper:
            start, end = upper_half(start, end)
        else:
            assert False
    assert start == end
    return start


def traverse_front_back(input, start, end):
    return traverse(input, "F", "B", start, end)


def traverse_left_right(input, start, end):
    return traverse(input, "L", "R", start, end)


def seat_id(row, column):
    return row * 8 + column


def seat(boarding_pass):
    row = traverse_front_back(boarding_pass[0:7], 0, 127)
    column = traverse_left_right(boarding_pass[7:], 0, 7)
    return seat_id(row, column)


def part_1(input):
    print(max(map(seat, input.splitlines())))


def sliding_pairs(iterable):
    iterator = iter(iterable)
    prev = next(iterator)
    for item in iterator:
        yield prev, item
        prev = item


def part_2(input):
    print(
        next(
            a + 1
            for a, b in sliding_pairs(sorted(map(seat, input.splitlines())))
            if a + 1 != b
        )
    )
