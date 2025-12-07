#!/usr/bin/env python

import functools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> tuple[Point, set[Point]]:
        start: Point | None = None
        splitters: set[Point] = set()
        for x, line in enumerate(input):
            for y, c in enumerate(line):
                pos = Point(x, y)
                if c == "S":
                    start = pos
                elif c == "^":
                    splitters.add(pos)
        assert start is not None
        return start, splitters

    def count_timelines(start: Point, splitters: set[Point]) -> int:
        max_x = max(p.x for p in splitters)

        @functools.cache
        def rec(p: Point) -> int:
            if p.x > max_x:
                return 1
            if p not in splitters:
                return rec(Point(p.x + 1, p.y))
            return rec(Point(p.x + 1, p.y - 1)) + rec(Point(p.x + 1, p.y + 1))

        return rec(start)

    start, splitters = parse(input)
    return count_timelines(start, splitters)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
