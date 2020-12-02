#!/usr/bin/env python

import re
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class Policy:
    min: int
    max: int
    letter: str


@dataclass
class Password:
    policy: Policy
    password: str


def is_valid(pwd: Password) -> bool:
    occurences = pwd.password.count(pwd.policy.letter)
    return pwd.policy.min <= occurences <= pwd.policy.max


def solve(passwords: List[Password]) -> int:
    return sum(map(is_valid, passwords))


def main() -> None:
    pattern = re.compile("([0-9]+)-([0-9]+) (.): (.+)")
    input = [
        Password(Policy(int(m.group(1)), int(m.group(2)), m.group(3)), m.group(4))
        for m in (pattern.match(line) for line in sys.stdin.readlines())
        if m
    ]
    print(solve(input))


if __name__ == "__main__":
    main()
