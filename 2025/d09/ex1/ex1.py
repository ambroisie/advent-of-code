#!/usr/bin/env python

import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> list[Point]:
        return [Point(*map(int, line.split(","))) for line in input]

    def rectangle_area(p: Point, other: Point) -> int:
        dx = abs(p.x - other.x)
        dy = abs(p.y - other.y)
        return (dx + 1) * (dy + 1)

    tiles = parse(input)
    return max(rectangle_area(a, b) for a, b in itertools.combinations(tiles, 2))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
