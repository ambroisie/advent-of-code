#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.StrEnum):
    NORTH_WEST = "nw"
    NORTH = "n"
    NORTH_EAST = "ne"
    SOUTH_EAST = "se"
    SOUTH = "s"
    SOUTH_WEST = "sw"

    # https://www.redblobgames.com/grids/hexagons/#coordinates-axial
    def apply(self, p: Point) -> Point:
        # (x, y) <=> (q, r)
        match self:
            case Direction.NORTH_WEST:
                dx, dy = -1, 0
            case Direction.NORTH:
                dx, dy = 0, -1
            case Direction.NORTH_EAST:
                dx, dy = 1, -1
            case Direction.SOUTH_EAST:
                dx, dy = 1, 0
            case Direction.SOUTH:
                dx, dy = 0, 1
            case Direction.SOUTH_WEST:
                dx, dy = -1, 1
        return Point(p.x + dx, p.y + dy)


def solve(input: str) -> int:
    def parse(input: str) -> list[Direction]:
        return [Direction(dir) for dir in input.strip().split(",")]

    # https://www.redblobgames.com/grids/hexagons/#distances-axial
    def hex_dist(a: Point, b: Point) -> int:
        dx, dy = a.x - b.x, a.y - b.y
        return (abs(dx) + abs(dx + dy) + abs(dy)) // 2

    directions = parse(input)
    pos = Point(0, 0)
    for dir in directions:
        pos = dir.apply(pos)
    return hex_dist(Point(0, 0), pos)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
