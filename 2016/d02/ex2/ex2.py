#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"

    def apply(self, p: Point) -> Point:
        match self:
            case Direction.UP:
                dx, dy = -1, 0
            case Direction.DOWN:
                dx, dy = 1, 0
            case Direction.LEFT:
                dx, dy = 0, -1
            case Direction.RIGHT:
                dx, dy = 0, 1
        return Point(p.x + dx, p.y + dy)


def solve(input: str) -> str:
    def parse(input: str) -> list[list[Direction]]:
        return [[Direction(c) for c in line] for line in input.splitlines()]

    def enter_code(directions: list[list[Direction]]) -> str:
        KEYPAD = {
            Point(-2, 2): "1",
            Point(-1, 1): "2",
            Point(-1, 2): "3",
            Point(-1, 3): "4",
            Point(0, 0): "5",
            Point(0, 1): "6",
            Point(0, 2): "7",
            Point(0, 3): "8",
            Point(0, 4): "9",
            Point(1, 1): "A",
            Point(1, 2): "B",
            Point(1, 3): "C",
            Point(2, 2): "D",
        }
        letters = []
        pos = Point(0, 0)
        for line in directions:
            for d in line:
                new_pos = d.apply(pos)
                if new_pos not in KEYPAD:
                    continue
                pos = new_pos
            letters.append(KEYPAD[pos])
        return "".join(letters)

    directions = parse(input)
    return enter_code(directions)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
