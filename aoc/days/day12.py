from dataclasses import dataclass


@dataclass
class Action:
    type: str
    value: int


def actions(input):
    return (Action(line[0], int(line[1:])) for line in input.splitlines())


def angle_to_dir(angle):
    return ["E", "N", "W", "S"][int(angle / 90 % 4)]


def step1(action, angle, x, y):
    if action.type == "N":
        return angle, x, y + action.value
    elif action.type == "S":
        return angle, x, y - action.value
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
        return step1(act, angle, x, y)
    assert False


def move(fn, actions, *args):
    for action in actions:
        args = fn(action, *args)
    return args


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def part_1(input):
    angle, x1, y1 = 0, 0, 0
    _, x2, y2 = move(step1, actions(input), angle, x1, y1)
    print(distance(x1, y1, x2, y2))


def rotate(angle, wx, wy):
    if angle == 0:
        return wx, wy
    elif angle == 90:
        return wy, -wx
    elif angle == 180:
        return -wx, -wy
    elif angle == 270:
        return -wy, wx
    assert False


def step2(action, wx, wy, sx, sy):
    if action.type == "N":
        return wx, wy + action.value, sx, sy
    elif action.type == "S":
        return wx, wy - action.value, sx, sy
    elif action.type == "E":
        return wx + action.value, wy, sx, sy
    elif action.type == "W":
        return wx - action.value, wy, sx, sy
    elif action.type == "L":
        return (*rotate(360 - action.value, wx, wy), sx, sy)
    elif action.type == "R":
        return (*rotate(action.value, wx, wy), sx, sy)
    elif action.type == "F":
        return wx, wy, sx + (wx * action.value), sy + (wy * action.value)
    assert False


def part_2(input):
    sx, sy = 0, 0
    wx, wy = 10, 1
    _, _, sx2, sy2 = move(step2, actions(input), wx, wy, sx, sy)
    print(distance(sx, sy, sx2, sy2))
