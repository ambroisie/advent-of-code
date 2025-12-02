#!/usr/bin/env python

import math
import sys
from collections.abc import Iterator


def solve(input: str) -> int:
    def parse_range(input: str) -> tuple[int, int]:
        start, end = input.split("-")
        return int(start), int(end)

    def parse(input: str) -> list[tuple[int, int]]:
        return [parse_range(r) for r in input.split(",")]

    def iter_invalids(start: int, end: int) -> Iterator[int]:
        for n in range(start, end):
            digits = int(math.log10(n)) + 1
            if digits % 2 == 1:
                continue
            base = 10 ** (digits // 2) + 1
            if n % base == 0:
                yield n

    ranges = parse(input)
    return sum(sum(iter_invalids(start, end + 1)) for start, end in ranges)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
