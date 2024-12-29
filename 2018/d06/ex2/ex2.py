#!/usr/bin/env python

import itertools
import sys
from collections import Counter
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def parse(input: list[str]) -> list[Point]:
        return [Point(*map(int, line.split(", "))) for line in input]

    def dist(lhs: Point, rhs: Point) -> int:
        return sum(abs(a - b) for a, b in zip(lhs, rhs))

    def points_distances(coords: list[Point]) -> dict[Point, Counter[Point]]:
        top_left = Point(min(p.x for p in coords), min(p.y for p in coords))
        bot_right = Point(max(p.x for p in coords), max(p.y for p in coords))

        return {
            p: Counter({root: dist(root, p) for root in coords})
            for p in map(
                Point._make,
                itertools.product(
                    range(top_left.x, bot_right.x + 1),
                    range(top_left.y, bot_right.y + 1),
                ),
            )
        }

    coords = parse(input.splitlines())
    distances = points_distances(coords)
    return sum(dist.total() < 10000 for dist in distances.values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
