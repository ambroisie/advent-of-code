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

    def merge_overlaps(ranges: list[Range]) -> list[Range]:
        # Sort ranges by start, then merge overlapping ones
        ranges = sorted(ranges)
        res = [ranges[0]]
        for interval in ranges[1:]:
            # `+ 1` to merge [0, 2] and [2, 5]
            if interval.start <= (res[-1].end + 1):
                res[-1] = Range(res[-1].start, max(interval.end, res[-1].end))
            else:
                res.append(interval)
        return res

    ranges, _ = parse(input)
    ranges = merge_overlaps(ranges)
    return sum(range.end - range.start + 1 for range in ranges)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
