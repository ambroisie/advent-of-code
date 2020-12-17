#!/usr/bin/env python

import itertools
import sys
from typing import Iterator, Set, Tuple

Point = Tuple[int, int, int, int]
Grid = Set[Point]


def update(grid: Grid) -> Grid:
    def neightbours(p: Point) -> Iterator[Point]:
        for dx, dy, dz, dw in itertools.product(range(-1, 2), repeat=4):
            if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                continue
            yield p[0] + dx, p[1] + dy, p[2] + dz, p[3] + dw

    def count_neighbours(p: Point) -> int:
        return sum(n in grid for n in neightbours(p))

    new_grid: Grid = set()
    seen: Set[Point] = set()
    for p in grid:
        for n in itertools.chain(neightbours(p), [p]):
            if n in seen:
                continue
            seen |= {n}
            active = n in grid
            num_neighbours = count_neighbours(n)

            if active and num_neighbours in [2, 3]:
                new_grid |= {n}
            elif active:
                continue
            elif num_neighbours == 3:
                new_grid |= {n}
            else:
                continue

    return new_grid


def solve(grid: Grid) -> int:

    for __ in range(6):
        grid = update(grid)

    return len(grid)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(
        solve(
            {
                (i, j, 0, 0)
                for i, line in enumerate(input)
                for j, x in enumerate(line)
                if x == "#"
            }
        )
    )


if __name__ == "__main__":
    main()
