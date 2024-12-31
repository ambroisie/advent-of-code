#!/usr/bin/env python

import enum
import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def neighbours(self) -> Iterator["Point"]:
        for dx, dy in itertools.product(range(-1, 1 + 1), repeat=2):
            if dx == 0 and dy == 0:
                continue
            yield Point(self.x + dx, self.y + dy)


class Cell(enum.StrEnum):
    OPEN = "."
    TREE = "|"
    LUMBERYARD = "#"


def solve(input: str) -> int:
    def parse(input: list[str]) -> dict[Point, Cell]:
        return {
            Point(x, y): Cell(c)
            for x, line in enumerate(input)
            for y, c in enumerate(line)
        }

    def step_cell(p: Point, grid: dict[Point, Cell]) -> Cell:
        neighbours = (n for n in p.neighbours() if n in grid)
        if grid[p] == Cell.OPEN:
            trees = sum(grid[n] == Cell.TREE for n in neighbours)
            return Cell.TREE if trees >= 3 else Cell.OPEN
        if grid[p] == Cell.TREE:
            lumberyards = sum(grid[n] == Cell.LUMBERYARD for n in neighbours)
            return Cell.LUMBERYARD if lumberyards >= 3 else Cell.TREE
        if grid[p] == Cell.LUMBERYARD:
            continues = {Cell.TREE, Cell.LUMBERYARD} <= {grid[n] for n in neighbours}
            return Cell.LUMBERYARD if continues else Cell.OPEN
        assert False  # Sanity check

    def step(grid: dict[Point, Cell]) -> dict[Point, Cell]:
        res: dict[Point, Cell] = {}
        for p in map(Point._make, itertools.product(range(50), repeat=2)):
            res[p] = step_cell(p, grid)
        return res

    def frozen(grid: dict[Point, Cell]) -> tuple[Cell, ...]:
        return tuple(grid[p] for p in sorted(grid.keys()))

    def thawed(hashed_grid: tuple[Cell, ...]) -> dict[Point, Cell]:
        return {Point(i // 50, i % 50): c for i, c in enumerate(hashed_grid)}

    def do_cycles(grid: dict[Point, Cell], end: int) -> dict[Point, Cell]:
        hashed_grid = frozen(grid)
        cache = {hashed_grid: 0}
        t = 0
        while t < end:
            hashed_grid = frozen(step(thawed(hashed_grid)))
            t += 1
            if hashed_grid in cache:
                previous_t = cache[hashed_grid]
                cycle_length = t - previous_t
                num_cycles = (end - t) // cycle_length
                t += num_cycles * cycle_length
            else:
                cache[hashed_grid] = t

        return thawed(hashed_grid)

    grid = parse(input.splitlines())
    grid = do_cycles(grid, 1000000000)
    trees = sum(c == Cell.TREE for c in grid.values())
    lumberyards = sum(c == Cell.LUMBERYARD for c in grid.values())
    return trees * lumberyards


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
