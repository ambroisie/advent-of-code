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

INNER_NEIGHBOURS = {
    Point(1, 2): {Point(0, y) for y in range(DIMS)},
    Point(3, 2): {Point(DIMS - 1, y) for y in range(DIMS)},
    Point(2, 1): {Point(x, 0) for x in range(DIMS)},
    Point(2, 3): {Point(x, DIMS - 1) for x in range(DIMS)},
}

X_OUTER_NEIGHBOUR = {
    p: n for n in (Point(1, 2), Point(3, 2)) for p in INNER_NEIGHBOURS[n]
}
Y_OUTER_NEIGHBOUR = {
    p: n for n in (Point(2, 1), Point(2, 3)) for p in INNER_NEIGHBOURS[n]
}


def solve(input: str) -> int:
    def parse(input: list[str]) -> set[tuple[Point, int]]:
        return {
            (Point(x, y), 0)
            for x, line in enumerate(input)
            for y, c in enumerate(line)
            if c == "#"
        }

    def grid_neighbours(p: Point, level: int) -> set[tuple[Point, int]]:
        assert p != Point(2, 2)  # Sanity check

        res: set[tuple[Point, int]] = set()
        for n in p.neighbours():
            if n == Point(2, 2):
                res |= {(n, level + 1) for n in INNER_NEIGHBOURS[p]}
            elif n.x in (-1, DIMS):
                res.add((X_OUTER_NEIGHBOUR[p], level - 1))
            elif n.y in (-1, DIMS):
                res.add((Y_OUTER_NEIGHBOUR[p], level - 1))
            else:
                res.add((n, level))

        return res

    def step(bugs: set[tuple[Point, int]]) -> set[tuple[Point, int]]:
        res: set[tuple[Point, int]] = set()
        min_level, max_level = (
            min(level for _, level in bugs),
            max(level for _, level in bugs),
        )
        for level in range(min_level - 1, max_level + 1 + 1):
            for p in map(Point._make, itertools.product(range(DIMS), range(DIMS))):
                if p == Point(2, 2):
                    continue
                neighbours = len(grid_neighbours(p, level) & bugs)
                # Bug dies if not exactly one neighbour
                if (p, level) in bugs and neighbours != 1:
                    continue
                # An empty space stays empty if it doesn't have 1 or 2 neighbours
                if (p, level) not in bugs and neighbours not in (1, 2):
                    continue
                res.add((p, level))
        return res

    bugs = parse(input.splitlines())
    for _ in range(200):
        bugs = step(bugs)
    return len(bugs)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
