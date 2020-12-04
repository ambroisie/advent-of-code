#!/usr/bin/env python

import sys
from typing import List


def validate(passport: List[str]) -> int:
    fields = [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    ]
    for field in fields:
        if field not in passport:
            return False
    return True


def solve(passport_fields: List[List[str]]) -> int:
    return sum(validate(passport) for passport in passport_fields)


def main() -> None:
    passports: List[List[str]] = [[]]
    for line in sys.stdin:
        if line == "\n" or line == "":
            passports.append([])
            continue
        passports[-1] += [s.split(":")[0] for s in line.split(" ")]
    print(solve(passports))


if __name__ == "__main__":
    main()
