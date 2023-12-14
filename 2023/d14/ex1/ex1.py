#!/usr/bin/env python

import itertools
import sys
from enum import StrEnum
from typing import NamedTuple, Optional


class Cell(StrEnum):
    ROLLER = "O"
    CUBE = "#"
    EMPTY = "."


class Map(NamedTuple):
    rocks: tuple[tuple[Optional[Cell], ...], ...]
    lines: int
    rows: int

    def tilt_north(self) -> "Map":
        rocks = [[Cell.EMPTY for _ in range(self.rows)] for _ in range(self.lines)]

        for y in range(self.rows):
            rolling_stop = -1

            for x in range(self.lines):
                # Nothing to do on empty cell
                if self.rocks[x][y] == Cell.EMPTY:
                    continue
                # Record the new stop point on cubes
                if self.rocks[x][y] == Cell.CUBE:
                    rolling_stop = x
                    rocks[x][y] = Cell.CUBE
                    continue
                # For rollers, roll it up to the `last_cube`
                rocks[rolling_stop + 1][y] = Cell.ROLLER
                rolling_stop += 1

        return Map(tuple(map(tuple, rocks)), self.lines, self.rows)

    def load(self) -> int:
        res = 0

        for x, y in itertools.product(range(self.lines), range(self.rows)):
            if self.rocks[x][y] != Cell.ROLLER:
                continue
            res += self.lines - x

        return res


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> Map:
        rocks = tuple(tuple(Cell(c) for c in line) for line in input)
        return Map(rocks, len(input), len(input[0]))

    map = parse(input)
    map = map.tilt_north()
    return map.load()


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
