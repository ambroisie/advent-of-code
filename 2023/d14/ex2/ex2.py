#!/usr/bin/env python

import dataclasses
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

    def tilt_south(self) -> "Map":
        rocks = [[Cell.EMPTY for _ in range(self.rows)] for _ in range(self.lines)]

        for y in range(self.rows):
            rolling_stop = self.rows

            for x in reversed(range(self.lines)):
                # Nothing to do on empty cell
                if self.rocks[x][y] == Cell.EMPTY:
                    continue
                # Record the new stop point on cubes
                if self.rocks[x][y] == Cell.CUBE:
                    rolling_stop = x
                    rocks[x][y] = Cell.CUBE
                    continue
                # For rollers, roll it up to the `last_cube`
                rocks[rolling_stop - 1][y] = Cell.ROLLER
                rolling_stop -= 1

        return Map(tuple(map(tuple, rocks)), self.lines, self.rows)

    def tilt_west(self) -> "Map":
        rocks = [[Cell.EMPTY for _ in range(self.rows)] for _ in range(self.lines)]

        for x in range(self.lines):
            rolling_stop = -1

            for y in range(self.rows):
                # Nothing to do on empty cell
                if self.rocks[x][y] == Cell.EMPTY:
                    continue
                # Record the new stop point on cubes
                if self.rocks[x][y] == Cell.CUBE:
                    rolling_stop = y
                    rocks[x][y] = Cell.CUBE
                    continue
                # For rollers, roll it up to the `last_cube`
                rocks[x][rolling_stop + 1] = Cell.ROLLER
                rolling_stop += 1

        return Map(tuple(map(tuple, rocks)), self.lines, self.rows)

    def tilt_east(self) -> "Map":
        rocks = [[Cell.EMPTY for _ in range(self.rows)] for _ in range(self.lines)]

        for x in range(self.lines):
            rolling_stop = self.lines

            for y in reversed(range(self.rows)):
                # Nothing to do on empty cell
                if self.rocks[x][y] == Cell.EMPTY:
                    continue
                # Record the new stop point on cubes
                if self.rocks[x][y] == Cell.CUBE:
                    rolling_stop = y
                    rocks[x][y] = Cell.CUBE
                    continue
                # For rollers, roll it up to the `last_cube`
                rocks[x][rolling_stop - 1] = Cell.ROLLER
                rolling_stop -= 1

        return Map(tuple(map(tuple, rocks)), self.lines, self.rows)

    def cycle(self) -> "Map":
        return self.tilt_north().tilt_west().tilt_south().tilt_east()

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

    def do_cycles(map: Map) -> Map:
        cache = {map: 0}
        t = 0
        SPIN_CYCLE_LENGTH = 1000000000
        while t < SPIN_CYCLE_LENGTH:
            map = map.cycle()
            t += 1
            if map in cache:
                previous_t = cache[map]
                cycle_length = t - previous_t
                num_cycles = (SPIN_CYCLE_LENGTH - t) // cycle_length
                t += num_cycles * cycle_length
            else:
                cache[map] = t

        return map

    map = parse(input)
    map = do_cycles(map)
    return map.load()


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
