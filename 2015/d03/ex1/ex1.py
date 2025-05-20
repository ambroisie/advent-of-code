#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.StrEnum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"

    def apply(self, p: Point) -> Point:
        match self:
            case Direction.NORTH:
                dx, dy = -1, 0
            case Direction.EAST:
                dx, dy = 0, 1
            case Direction.SOUTH:
                dx, dy = 1, 0
            case Direction.WEST:
                dx, dy = 0, -1
        return Point(p.x + dx, p.y + dy)


def solve(input: str) -> int:
    def parse(input: str) -> list[Direction]:
        return [Direction(c) for c in input.strip()]

    def distribute_presents(moves: list[Direction]) -> set[Point]:
        pos = Point(0, 0)
        seen = {pos}
        for move in moves:
            pos = move.apply(pos)
            seen.add(pos)
        return seen

    moves = parse(input)
    presents = distribute_presents(moves)
    return len(presents)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
