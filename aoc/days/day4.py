import re


def year(value):
    return re.fullmatch(r"\d{4}", value) is not None


def birth_year(value):
    return year(value) and 1920 <= int(value) <= 2002


def issue_year(value):
    return year(value) and 2010 <= int(value) <= 2020


def expiration_year(value):
    return year(value) and 2020 <= int(value) <= 2030


def height(value):
    match = re.fullmatch(r"(\d+)(cm|in)", value)
    if match is not None:
        num = int(match.group(1))
        unit = match.group(2)
        if unit == "cm":
            return 150 <= num <= 193
        elif unit == "in":
            return 59 <= num <= 76
    return False


def hair_color(value):
    return re.fullmatch(r"#[0-9a-f]{6}", value) is not None


EYE_COLORS = frozenset({"amb", "blu", "brn", "gry", "grn", "hzl", "oth"})


def eye_color(value):
    return value in EYE_COLORS


def passport_id(value):
    return re.fullmatch(r"\d{9}", value) is not None


FIELDS = {
    "byr": birth_year,
    "iyr": issue_year,
    "eyr": expiration_year,
    "hgt": height,
    "hcl": hair_color,
    "ecl": eye_color,
    "pid": passport_id,
}


def parse_passports(input):
    current = {}
    for line in input.splitlines():
        if not line:
            if current:
                yield current
                current = {}
        else:
            current.update(kv.split(":", 2) for kv in line.split(" "))
    if current:
        yield current


def all_fields(passport):
    return FIELDS.keys() <= passport.keys()


def validate_passport(passport):
    return all_fields(passport) and all(
        validator(passport[field]) for field, validator in FIELDS.items()
    )


def part_1(input):
    print(sum(all_fields(passport) for passport in parse_passports(input)))


def part_2(input):
    print(sum(validate_passport(passport) for passport in parse_passports(input)))
