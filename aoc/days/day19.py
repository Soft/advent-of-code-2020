import re
from itertools import takewhile
from functools import partial

LIT_RE = re.compile(r"(\d+): \"(.)\"")
ALIAS_RE = re.compile(r"(\d+): (\d+)")
SEQ_RE = re.compile(r"(\d+): (\d+) (\d+)")
ALT1_RE = re.compile(r"(\d+): (\d+) \| (\d+)")
ALT2_RE = re.compile(r"(\d+): (\d+) (\d+) \| (\d+) (\d+)")


def identity(n):
    return n


def literal(c):
    def matcher(s):
        if len(s) >= 1 and s[0] == c:
            return s[1:]

    return matcher


def alias(rules, r):
    def matcher(s):
        return rules[r](s)

    return matcher


def seq(rules, r1, r2):
    def matcher(s):
        if (s := rules[r1](s)) is not None:
            return rules[r2](s)

    return matcher


def alt1(rules, ra, rb):
    def matcher(s):
        if (s1 := rules[ra](s)) is not None:
            return s1
        if (s1 := rules[rb](s)) is not None:
            return s1

    return matcher


def alt2(rules, ra1, ra2, rb1, rb2):
    def matcher(s):
        if (s1 := rules[ra1](s)) is not None and (
            s2 := rules[ra2](s1)
        ) is not None:
            return s2
        if (s1 := rules[rb1](s)) is not None and (
            s2 := rules[rb2](s1)
        ) is not None:
            return s2

    return matcher


def parse_rule(rules, line):
    if (match := LIT_RE.fullmatch(line)) is not None:
        return int(match.group(1)), literal(match.group(2))
    elif (match := ALIAS_RE.fullmatch(line)) is not None:
        return int(match.group(1)), alias(rules, int(match.group(2)))
    elif (match := SEQ_RE.fullmatch(line)) is not None:
        return (
            int(match.group(1)),
            seq(rules, int(match.group(2)), int(match.group(3))),
        )
    elif (match := ALT1_RE.fullmatch(line)) is not None:
        return (
            int(match.group(1)),
            alt1(rules, int(match.group(2)), int(match.group(3))),
        )
    elif (match := ALT2_RE.fullmatch(line)) is not None:
        return (
            int(match.group(1)),
            alt2(
                rules,
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4)),
                int(match.group(5)),
            ),
        )
    else:
        assert False


def parse_rules(lines):
    rules = {}
    rules.update(
        parse_rule(rules, line) for line in takewhile(identity, lines)
    )
    return rules


def parse(input):
    lines = iter(input.splitlines())
    rules = parse_rules(lines)
    return rules, list(lines)


def match(matcher, s):
    return matcher(s) == ""


def part_1(input):
    rules, messages = parse(input)
    matcher = partial(match, rules[0])
    print(sum(map(matcher, messages)))
