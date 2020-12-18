from operator import add, mul


def evaluate(expression, subexpr=False):
    chars = iter(expression)
    acc = None
    operator = None
    for c in chars:
        if c.isspace():
            continue
        elif c.isdigit() and acc is None:
            acc = int(c)
        elif c.isdigit() and operator is not None:
            acc = operator(acc, int(c))
            operator = None
        elif c == "+" and operator is None and acc is not None:
            operator = add
        elif c == "*" and operator is None and acc is not None:
            operator = mul
        elif c == "(" and acc is None:
            acc = evaluate(chars, True)
        elif c == "(" and operator is not None:
            acc = operator(acc, evaluate(chars, True))
            operator = None
        elif c == ")" and subexpr:
            return acc
        else:
            assert False
    assert operator is None and acc is not None
    return acc


def part_1(input):
    print(sum(map(evaluate, input.splitlines())))
