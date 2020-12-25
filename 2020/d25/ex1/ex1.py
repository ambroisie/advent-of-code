#!/usr/bin/env python

import itertools
import sys
from typing import List


def step(value: int, subject: int) -> int:
    value *= subject
    value %= 20201227
    return value


def solve(raw: List[int]) -> int:
    value = 1

    for rounds in itertools.count(1):
        value = step(value, 7)
        if value == raw[0]:
            break

    key = 1
    for __ in range(rounds):
        key = step(key, raw[1])

    return key


def main() -> None:
    input = [int(line) for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
