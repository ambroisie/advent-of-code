#!/usr/bin/env python

import enum
import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Region(enum.IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2


def solve(input: str) -> int:
    def parse(input: list[str]) -> tuple[int, Point]:
        depth = input[0].removeprefix("depth: ")
        target = input[1].removeprefix("target: ")
        return int(depth), Point(*(int(n) for n in target.split(",")))

    def compute_erosions(depth: int, target: Point) -> dict[Point, int]:
        res: dict[Point, int] = {}
        for x in range(0, target.x + 1):
            for y in range(0, target.y + 1):
                p = Point(x, y)
                if p == Point(0, 0) or p == target:
                    res[p] = 0
                elif p.y == 0:
                    res[p] = p.x * 16807
                elif p.x == 0:
                    res[p] = p.y * 48271
                else:
                    res[p] = res[Point(p.x - 1, p.y)] * res[Point(p.x, p.y - 1)]
                # Go from geologic index to erosion level
                res[p] += depth
                res[p] %= 20183
        return res

    def compute_regions(depth: int, target: Point) -> dict[Point, Region]:
        return {
            p: Region(erosion % 3)
            for p, erosion in compute_erosions(depth, target).items()
        }

    depth, target = parse(input.splitlines())
    regions = compute_regions(depth, target)
    return sum(
        regions[p]
        for p in map(
            Point._make,
            itertools.product(range(0, target.x + 1), range(target.y + 1)),
        )
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
