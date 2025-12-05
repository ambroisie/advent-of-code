#!/usr/bin/env python

import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> set[Point]:
        return {
            Point(x, y)
            for x, line in enumerate(input)
            for y, c in enumerate(line)
            if c == "@"
        }

    def is_accessible(point: Point, rolls: set[Point]) -> bool:
        assert point in rolls  # Sanity check
        return (
            sum(
                Point(point.x + dx, point.y + dy) in rolls
                for dx, dy in itertools.product(range(-1, 1 + 1), repeat=2)
                if dx != 0 or dy != 0
            )
            < 4
        )

    rolls = parse(input)
    removed = 0
    while accessible := {p for p in rolls if is_accessible(p, rolls)}:
        removed += len(accessible)
        rolls -= accessible
    return removed


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
