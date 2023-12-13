#!/usr/bin/env python

import sys
from typing import NamedTuple, Optional


class Point(NamedTuple):
    x: int
    y: int


class Grid(NamedTuple):
    points: set[Point]
    lines: int
    rows: int


def solve(input: str) -> int:
    def parse_grid(grid: list[str]) -> Grid:
        points: set[Point] = set()

        for x, line in enumerate(grid):
            for y, c in enumerate(line):
                if c != "#":
                    continue
                points.add(Point(x, y))

        return Grid(points, len(grid), len(grid[0]))

    def parse(input: str) -> list[Grid]:
        return [parse_grid(grid.splitlines()) for grid in input.split("\n\n")]

    def reflect_vertical(grid: Grid) -> Optional[int]:
        def try_row(row: int) -> set[Point]:
            smudges: set[Point] = set()
            for y in range(min(row, grid.rows - row)):
                for x in range(grid.lines):
                    left = Point(x, row - y - 1) in grid.points
                    right = Point(x, row + y) in grid.points
                    if left and right:
                        continue
                    if left or right:
                        smudges.add(Point(x, row - y - 1))
            return smudges

        for row in range(1, grid.rows):
            if len(try_row(row)) == 1:
                return row
        return None

    def reflect_horizontal(grid: Grid) -> Optional[int]:
        def try_line(line: int) -> set[Point]:
            smudges: set[Point] = set()
            for x in range(min(line, grid.lines - line)):
                for y in range(grid.rows):
                    up = Point(line - x - 1, y) in grid.points
                    down = Point(line + x, y) in grid.points
                    if up and down:
                        continue
                    if up or down:
                        smudges.add(Point(line - x - 1, y))
            return smudges

        for line in range(1, grid.lines):
            if len(try_line(line)) == 1:
                return line
        return None

    def solve(grid: Grid) -> int:
        if (columns := reflect_vertical(grid)) is not None:
            return columns
        if (rows := reflect_horizontal(grid)) is not None:
            return 100 * rows
        assert False  # Sanity check

    grids = parse(input)
    return sum(map(solve, grids))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
