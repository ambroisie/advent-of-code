#!/usr/bin/env python

import dataclasses
import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple, Optional


def sign(n: int) -> int:
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_input(cls, input: str) -> "Point":
        x, y = input.split(",")
        return cls(int(x), int(y))


@dataclasses.dataclass
class Line:
    points: list[Point]

    @classmethod
    def from_input(cls, input: str) -> "Line":
        points = [Point.from_input(p) for p in input.split(" -> ")]
        return cls(points)

    @property
    def all_points(self) -> set[Point]:
        res: set[Point] = set()

        for start, end in itertools.pairwise(self.points):
            dx, dy = sign(end.x - start.x), sign(end.y - start.y)
            res.add(start)
            while start != end:
                start = Point(start.x + dx, start.y + dy)
                res.add(start)

        return res


def solve(input: list[str]) -> int:
    lines = [Line.from_input(line) for line in input]
    all_points = set.union(*(line.all_points for line in lines))
    max_height = max(p.y for p in all_points)

    def sand_candidates(p: Point) -> Iterator[Point]:
        for dx, dy in ((0, 1), (-1, 1), (1, 1)):
            yield Point(p.x + dx, p.y + dy)

    def add_sand(points: set[Point]) -> Optional[Point]:
        start = Point(500, 0)

        assert start not in points  # Sanity check

        while True:
            # Steady state was reached
            if start.y >= max_height:
                return None

            viable_candidates = (p for p in sand_candidates(start) if p not in points)
            candidate = next(viable_candidates, None)
            # Sand can't fall any lower
            if candidate is None:
                break
            start = candidate

        return start

    res = 0
    while True:
        grain = add_sand(all_points)
        if grain is None:
            break
        all_points.add(grain)
        res += 1
    return res


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
