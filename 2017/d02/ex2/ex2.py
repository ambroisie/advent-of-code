#!/usr/bin/env python

import itertools
import sys


def solve(input: str) -> int:
    def parse(input: str) -> list[list[int]]:
        return [[int(n) for n in line.split()] for line in input.splitlines()]

    def evenly_divide(row: list[int]) -> int:
        for a, b in itertools.combinations(sorted(row), 2):
            assert a <= b  # Sanity check
            if b % a:
                continue
            return b // a
        assert False  # Sanity check

    sheet = parse(input)
    return sum(map(evenly_divide, sheet))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
