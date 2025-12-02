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
            for repeat in range(2, digits + 1):
                if digits % repeat != 0:
                    continue
                cycle = digits // repeat
                base = (10**digits - 1) // (10**cycle - 1)
                if n % base == 0:
                    yield n
                    break  # Don't yield the same digit twice

    ranges = parse(input)
    return sum(sum(iter_invalids(start, end + 1)) for start, end in ranges)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
