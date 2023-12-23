#!/usr/bin/env python

import enum
import sys
from collections.abc import Iterator
from typing import NamedTuple, Optional


class Point(NamedTuple):
    x: int
    y: int


class Cell(enum.StrEnum):
    PATH = "."
    NORTH_SLOPE = "^"
    SOUTH_SLOPE = "v"
    WEST_SLOPE = "<"
    EAST_SLOPE = ">"

    def neighbours(self) -> Iterator[Point]:
        match self:
            case self.PATH:
                yield from (
                    Point(-1, 0),
                    Point(1, 0),
                    Point(0, -1),
                    Point(0, 1),
                )
            case self.NORTH_SLOPE:
                yield Point(-1, 0)
            case self.SOUTH_SLOPE:
                yield Point(1, 0)
            case self.WEST_SLOPE:
                yield Point(0, -1)
            case self.EAST_SLOPE:
                yield Point(0, 1)

    def apply(self, pos: Point) -> Iterator[Point]:
        for dx, dy in self.neighbours():
            yield Point(pos.x + dx, pos.y + dy)


Trails = dict[Point, Cell]


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> Trails:
        res: Trails = {}

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == "#":
                    continue
                res[Point(x, y)] = Cell(c)

        return res

    def explore(trails: Trails, start: Point, dest: Point) -> int:
        def recurse(start: Point, seen: set[Point]) -> Optional[int]:
            if start == dest:
                return 0
            if start not in trails:
                return None
            next_step = (
                recurse(n, seen | {n})
                for n in trails[start].apply(start)
                if n not in seen
            )
            distances = [dist for dist in next_step if dist is not None]
            if not distances:
                return None
            return max(distances) + 1

        res = recurse(start, {start})
        assert res is not None  # Sanity check
        return res

    trails = parse(input)
    start, dest = Point(0, 1), Point(len(input) - 1, len(input[0]) - 2)
    assert start in trails  # Sanity check
    assert dest in trails  # Sanity check
    sys.setrecursionlimit(10_000)
    return explore(trails, start, dest)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
