#!/usr/bin/env python

import sys
from typing import NamedTuple


class Interval(NamedTuple):
    start: int
    end: int

    @classmethod
    def from_str(cls, input: str) -> "Interval":
        start, end = input.split("-")
        return cls(int(start), int(end))


def solve(input: str) -> int:
    def parse(input: str) -> list[Interval]:
        return [Interval.from_str(line) for line in input.splitlines()]

    def merge_overlaps(intervals: list[Interval]) -> list[Interval]:
        # Sort intervals by start, then merge overlapping ones
        intervals = sorted(intervals)
        res = [intervals[0]]
        for interval in intervals[1:]:
            # `+ 1` to merge [0, 2] and [2, 5]
            if interval.start <= (res[-1].end + 1):
                res[-1] = Interval(res[-1].start, max(interval.end, res[-1].end))
            else:
                res.append(interval)
        return res

    intervals = parse(input)
    intervals = merge_overlaps(intervals)
    return (1 << 32) - sum((end - start + 1) for start, end in intervals)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
