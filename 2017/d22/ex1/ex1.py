#!/usr/bin/env python

import dataclasses
import enum
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.Enum):
    UP = Point(-1, 0)
    DOWN = Point(1, 0)
    LEFT = Point(0, -1)
    RIGHT = Point(0, 1)

    def left(self) -> "Direction":
        x, y = self.value
        return Direction(Point(-y, x))

    def right(self) -> "Direction":
        x, y = self.value
        return Direction(Point(y, -x))

    def apply(self, p: Point) -> Point:
        dx, dy = self.value
        return Point(p.x + dx, p.y + dy)


@dataclasses.dataclass
class Carrier:
    pos: Point
    dir: Direction

    def burst(self, infected: set[Point]) -> bool:
        infect = False
        if self.pos in infected:
            self.dir = self.dir.right()
            infected.remove(self.pos)
        else:
            self.dir = self.dir.left()
            infected.add(self.pos)
            infect = True
        self.pos = self.dir.apply(self.pos)
        return infect


def solve(input: str) -> int:
    def parse(input: str) -> set[Point]:
        return {
            Point(x, y)
            for x, line in enumerate(input.splitlines())
            for y, c in enumerate(line)
            if c == "#"
        }

    infected = parse(input)
    middle = len(input.splitlines()) // 2
    carrier = Carrier(Point(middle, middle), Direction.UP)
    total = 0

    for _ in range(10000):
        total += carrier.burst(infected)
    return total


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
