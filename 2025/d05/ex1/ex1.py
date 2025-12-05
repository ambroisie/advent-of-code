#!/usr/bin/env python

import sys
from typing import NamedTuple


class Range(NamedTuple):
    start: int
    end: int

    @classmethod
    def from_str(cls, input: str) -> "Range":
        start, end = input.split("-")
        return cls(int(start), int(end))

    def contains(self, point: int) -> bool:
        return self.start <= point <= self.end


def solve(input: str) -> int:
    def parse(input: str) -> tuple[list[Range], list[int]]:
        ranges, ids = input.split("\n\n")
        return [Range.from_str(r) for r in ranges.splitlines()], [
            int(n) for n in ids.splitlines()
        ]

    ranges, ids = parse(input)
    return sum(any(range.contains(id) for range in ranges) for id in ids)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
