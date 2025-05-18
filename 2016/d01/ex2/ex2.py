#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.Enum):
    NORTH = Point(-1, 0)
    EAST = Point(0, 1)
    SOUTH = Point(1, 0)
    WEST = Point(0, -1)

    def left(self) -> "Direction":
        match self:
            case Direction.NORTH:
                return Direction.WEST
            case Direction.EAST:
                return Direction.NORTH
            case Direction.SOUTH:
                return Direction.EAST
            case Direction.WEST:
                return Direction.SOUTH

    def right(self) -> "Direction":
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH

    def apply(self, p: Point, n: int = 1) -> Point:
        dx, dy = self.value
        return Point(p.x + dx * n, p.y + dy * n)


def solve(input: str) -> int:
    def parse(input: str) -> list[tuple[str, int]]:
        return [((line[0]), int(line[1:])) for line in input.split(", ")]

    def first_repeat(directions: list[tuple[str, int]]) -> Point:
        pos, dir = Point(0, 0), Direction.NORTH
        directions = parse(input)
        seen = {pos}
        for turn, length in directions:
            dir = dir.left() if turn == "L" else dir.right()
            for _ in range(length):
                pos = dir.apply(pos)
                if pos in seen:
                    return pos
                seen.add(pos)
        assert False  # Sanity check

    directions = parse(input)
    pos = first_repeat(directions)
    return abs(pos.x) + abs(pos.y)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
