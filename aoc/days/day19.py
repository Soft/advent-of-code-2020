import re
from itertools import takewhile
from functools import partial

LIT_RE = re.compile(r"(\d+): \"(.)\"")
SEQ_RE = re.compile(r"(\d+): ((?:\d+)(?: (?:\d+))*)")
ALT_RE = re.compile(r"(\d+): ((?:\d+)(?: (?:\d+))*) \| ((?:\d+)(?: (?:\d+))*)")


def identity(n):
    return n


def ref(rules, i):
    def matcher(s):
        return rules[i](s)

    return matcher


def literal(c):
    def matcher(s):
        if len(s) >= 1 and s[0] == c:
            return s[1:]

    return matcher


def seq(*rs):
    def matcher(s):
        for r in rs:
            if (s := r(s)) is None:
                break
        return s

    return matcher


def alt(ra, rb):
    def matcher(s):
        if (s1 := ra(s)) is not None:
            return s1
        if (s1 := rb(s)) is not None:
            return s1

    return matcher


def parse_rule(rules, line):
    def parse_seq(s):
        return seq(*(ref(rules, int(r)) for r in s.split(" ")))

    if (match := LIT_RE.fullmatch(line)) is not None:
        return int(match.group(1)), literal(match.group(2))
    elif (match := SEQ_RE.fullmatch(line)) is not None:
        return (
            int(match.group(1)),
            parse_seq(match.group(2)),
        )
    elif (match := ALT_RE.fullmatch(line)) is not None:
        return (
            int(match.group(1)),
            alt(parse_seq(match.group(2)), parse_seq(match.group(3)),),
        )
    assert False


def parse_rules(lines):
    rules = {}
    rules.update(parse_rule(rules, line) for line in takewhile(identity, lines))
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
