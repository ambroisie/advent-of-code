#!/usr/bin/env python

import dataclasses
import sys
from collections.abc import Iterator


@dataclasses.dataclass
class Point:
    x: int
    y: int


def solve(input: list[list[int]]) -> int:
    def up(p: Point) -> Iterator[Point]:
        x = p.x
        while (x := x - 1) >= 0:
            yield Point(x, p.y)

    def down(p: Point) -> Iterator[Point]:
        x = p.x
        while (x := x + 1) < len(input):
            yield Point(x, p.y)

    def left(p: Point) -> Iterator[Point]:
        y = p.y
        while (y := y - 1) >= 0:
            yield Point(p.x, y)

    def right(p: Point) -> Iterator[Point]:
        y = p.y
        while (y := y + 1) < len(input[0]):
            yield Point(p.x, y)

    def is_visible(p: Point) -> bool:
        height = input[p.x][p.y]
        for neighbours in (up, down, left, right):
            if all(input[n.x][n.y] < height for n in neighbours(p)):
                return True
        return False

    visibility = [
        [is_visible(Point(x, y)) for y in range(len(input[x]))]
        for x in range(len(input))
    ]
    return sum(map(sum, visibility))


def main() -> None:
    input = [[int(c) for c in line] for line in sys.stdin.read().splitlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
