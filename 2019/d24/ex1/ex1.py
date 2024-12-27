#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def neighbours(self) -> Iterator["Point"]:
        for dx, dy in (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ):
            yield Point(self.x + dx, self.y + dy)


DIMS = 5


def solve(input: str) -> int:
    def parse(input: list[str]) -> frozenset[Point]:
        return frozenset(
            Point(x, y)
            for x, line in enumerate(input)
            for y, c in enumerate(line)
            if c == "#"
        )

    def step(bugs: frozenset[Point]) -> frozenset[Point]:
        res: set[Point] = set()
        for p in map(Point._make, itertools.product(range(DIMS), range(DIMS))):
            neighbours = len(set(p.neighbours()) & bugs)
            # Bug dies if not exactly one neighbour
            if p in bugs and neighbours != 1:
                continue
            # An empty space stays empty if it doesn't have 1 or 2 neighbours
            if p not in bugs and neighbours not in (1, 2):
                continue
            res.add(p)
        return frozenset(res)

    def biodiversity(bugs: frozenset[Point]) -> int:
        res = 0
        for x, y in itertools.product(range(DIMS), range(DIMS)):
            res |= (Point(x, y) in bugs) << (x * DIMS + y)
        return res

    bugs = parse(input.splitlines())
    layouts: set[frozenset[Point]] = set()

    while True:
        layouts.add(frozenset(bugs))
        bugs = step(bugs)
        if bugs in layouts:
            return biodiversity(bugs)

    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
