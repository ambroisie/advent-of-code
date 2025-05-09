#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse(input: str) -> list[list[int]]:
        return [[int(n) for n in line.split()] for line in input.splitlines()]

    def checksum(row: list[int]) -> int:
        return max(row) - min(row)

    sheet = parse(input)
    return sum(map(checksum, sheet))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
