#!/usr/bin/env python

import itertools
import sys
from copy import deepcopy
from typing import Iterator, List, Set, Tuple

Grid = List[List[int]]
Point = Tuple[int, int]


def solve(input: List[str]) -> int:
    levels = [[int(c) for c in line] for line in input]

    def step(levels: Grid) -> Tuple[Grid, int]:
        # First step, increase levels
        levels = [[l + 1 for l in line] for line in levels]

        def excited(levels: Grid) -> Set[Point]:
            return set(
                (i, j)
                for i in range(len(levels))
                for j in range(len(levels[i]))
                if levels[i][j] > 9
            )

        def neighbours_of(point: Point) -> Iterator[Point]:
            for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                if dx == 0 and dy == 0:
                    continue
                x = point[0] + dx
                y = point[1] + dy
                if x < 0 or x >= len(levels):
                    continue
                if y < 0 or y >= len(levels[x]):
                    continue
                yield x, y

        # Second step, do flashes
        has_flashed: Set[Point] = set()
        while len(flashes := (excited(levels) - has_flashed)) > 0:
            for i, j in flashes:
                has_flashed.add((i, j))
                for x, y in neighbours_of((i, j)):
                    levels[x][y] += 1

        # Finally, bring back energy levels to 0
        for i, j in has_flashed:
            levels[i][j] = 0

        return levels, len(has_flashed)

    res = 0
    for __ in range(100):
        levels, flashes = step(levels)
        res += flashes
    return res


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
