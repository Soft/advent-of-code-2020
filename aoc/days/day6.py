def groups(input):
    group = []
    for line in input.splitlines():
        if not line:
            yield group
            group = []
        else:
            group.append(frozenset(line))
    if group:
        yield group


def any_yes(group):
    return group.pop().union(*group)


def part_1(input):
    print(sum(len(any_yes(group)) for group in groups(input)))


def all_yes(group):
    return group.pop().intersection(*group)


def part_2(input):
    print(sum(len(all_yes(group)) for group in groups(input)))
