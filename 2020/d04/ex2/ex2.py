#!/usr/bin/env python

import re
import sys
from typing import List, Tuple

Field = Tuple[str, ...]


def validate_byr(field: str) -> bool:
    pattern = "^[0-9]{4}$"
    if not re.fullmatch(pattern, field):
        return False
    val = int(field)
    return 1920 <= val <= 2002


def validate_iyr(field: str) -> bool:
    pattern = "^[0-9]{4}$"
    if not re.fullmatch(pattern, field):
        return False
    val = int(field)
    return 2010 <= val <= 2020


def validate_eyr(field: str) -> bool:
    pattern = "^[0-9]{4}$"
    if not re.fullmatch(pattern, field):
        return False
    val = int(field)
    return 2020 <= val <= 2030


def validate_hgt(field: str) -> bool:
    pattern = "^[0-9]+(cm|in)$"
    if not re.fullmatch(pattern, field):
        return False
    val = int(field[:-2])
    if "cm" in field:
        return 150 <= val <= 193
    return 59 <= val <= 76


def validate_hcl(field: str) -> bool:
    pattern = "^#[a-f0-9]{6}$"
    if not re.fullmatch(pattern, field):
        return False
    return True


def validate_ecl(field: str) -> bool:
    return field in {
        "amb",
        "blu",
        "brn",
        "gry",
        "grn",
        "hzl",
        "oth",
    }


def validate_pid(field: str) -> bool:
    pattern = "^[0-9]{9}$"
    if not re.fullmatch(pattern, field):
        return False
    return True


def validate(passport: List[Field]) -> int:
    fields = {
        "byr": validate_byr,
        "iyr": validate_iyr,
        "eyr": validate_eyr,
        "hgt": validate_hgt,
        "hcl": validate_hcl,
        "ecl": validate_ecl,
        "pid": validate_pid,
    }
    tot = 0
    for field in passport:
        if len(field) != 2:
            continue
        if field[0] not in fields:
            if field[0] == "cid":
                continue
            return False
        if not fields[field[0]](field[1].strip()):
            return False
        tot += 1
    return tot == len(fields)


def solve(passport_fields: List[List[Field]]) -> int:
    return sum(validate(passport) for passport in passport_fields)


def main() -> None:
    passports: List[List[Field]] = [[]]
    for line in sys.stdin:
        if line == "\n" or line == "":
            passports.append([])
            continue
        passports[-1] += [tuple(s.split(":")) for s in line.split(" ") if s]
    print(solve(passports))


if __name__ == "__main__":
    main()
