from itertools import islice, count, cycle


def count_trees(input, x_step, y_step):
    trees = 0
    for x, line in zip(
        count(0, x_step), islice(input.splitlines(), None, None, y_step)
    ):
        if next(islice(cycle(line), x, x + 1)) == "#":
            trees += 1
    return trees


def part_1(input):
    print(count_trees(input, 3, 1))


def part_2(input):
    print(
        count_trees(input, 1, 1)
        * count_trees(input, 3, 1)
        * count_trees(input, 5, 1)
        * count_trees(input, 7, 1)
        * count_trees(input, 1, 2)
    )
