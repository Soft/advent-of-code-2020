from dataclasses import dataclass
from functools import partial
from operator import add, mul
from typing import Callable, List


@dataclass
class Operator:
    precedence: int
    fn: Callable[[List[int]], None]


def stackfn(fn):
    def wrap(queue):
        assert len(queue) >= 2
        queue.append(fn(queue.pop(), queue.pop()))

    return wrap


def evaluate(operators, expression):
    output = []
    operator = []
    for c in expression:
        if c.isspace():
            continue
        elif c.isdigit():
            output.append(int(c))
        elif c in operators:
            while (
                operator
                and operator[-1] != "("
                and operators[operator[-1]].precedence >= operators[c].precedence
            ):
                operators[operator.pop()].fn(output)
            operator.append(c)
        elif c == "(":
            operator.append(c)
        elif c == ")":
            while operator[-1] != "(":
                operators[operator.pop()].fn(output)
            if operator[-1] == "(":
                operator.pop()
        else:
            assert False
    while operator:
        operators[operator.pop()].fn(output)
    return output[0]


def part_1(input):
    operators = {
        "+": Operator(1, stackfn(add)),
        "*": Operator(1, stackfn(mul)),
    }
    evaluate_ = partial(evaluate, operators)
    print(sum(map(evaluate_, input.splitlines())))


def part_2(input):
    operators = {
        "+": Operator(2, stackfn(add)),
        "*": Operator(1, stackfn(mul)),
    }
    evaluate_ = partial(evaluate, operators)
    print(sum(map(evaluate_, input.splitlines())))
