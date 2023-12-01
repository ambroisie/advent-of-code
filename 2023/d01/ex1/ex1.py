#!/usr/bin/env python

import sys


def solve(input: list[str]) -> int:
    def value(line: str) -> int:
        digits = [int(c) for c in line if c.isdigit()]
        return digits[0] * 10 + digits[-1]

    return sum(value(line) for line in input)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
