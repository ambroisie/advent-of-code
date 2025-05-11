#!/usr/bin/env python

import enum
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.Enum):
    UP = Point(-1, 0)
    DOWN = Point(1, 0)
    LEFT = Point(0, -1)
    RIGHT = Point(0, 1)

    def apply(self, p: Point) -> Point:
        dx, dy = self.value
        return Point(p.x + dx, p.y + dy)

    def turns(self) -> Iterator["Direction"]:
        match self:
            case Direction.UP | Direction.DOWN:
                turns = (Direction.LEFT, Direction.RIGHT)
            case Direction.LEFT | Direction.RIGHT:
                turns = (Direction.UP, Direction.DOWN)
        yield from turns


def solve(input: str) -> int:
    def parse(input: str) -> dict[Point, str]:
        return {
            Point(x, y): c
            for x, line in enumerate(input.splitlines())
            for y, c in enumerate(line)
            if c != " "
        }

    def packet_walk(map: dict[Point, str]) -> int:
        letters: list[str] = []
        # Travel starts downward, from outside the map before the first line
        pos = min(map.keys(), key=lambda p: p.x)
        dir = Direction.DOWN

        steps = 0
        while True:
            if (letter := map[pos]) not in ("+", "|", "-"):
                letters.append(letter)
            new_dir = dir
            new_pos = dir.apply(pos)
            steps += 1
            if new_pos not in map:
                for new_dir in dir.turns():
                    if (new_pos := new_dir.apply(pos)) in map:
                        break
                else:
                    # Must be the end of the line, stop looping
                    return steps
            dir = new_dir
            pos = new_pos

    map = parse(input)
    return packet_walk(map)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
