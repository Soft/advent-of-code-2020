from dataclasses import dataclass


@dataclass
class Action:
    type: str
    value: int


def actions(input):
    return (Action(line[0], int(line[1:])) for line in input.splitlines())


def angle_to_dir(angle):
    return ["E", "N", "W", "S"][int(angle / 90 % 4)]


def step(action, angle, x, y):
    if action.type == "N":
        return angle, x, y - action.value
    elif action.type == "S":
        return angle, x, y + action.value
    elif action.type == "E":
        return angle, x + action.value, y
    elif action.type == "W":
        return angle, x - action.value, y
    elif action.type == "L":
        return angle + action.value, x, y
    elif action.type == "R":
        return angle - action.value, x, y
    elif action.type == "F":
        act = Action(angle_to_dir(angle), action.value)
        return step(act, angle, x, y)
    assert False


def move(actions, angle, x, y):
    for action in actions:
        angle, x, y = step(action, angle, x, y)
    return angle, x, y


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def part_1(input):
    angle, x1, y1 = 0, 0, 0
    _, x2, y2 = move(actions(input), angle, x1, y1)
    print(distance(x1, y1, x2, y2))
