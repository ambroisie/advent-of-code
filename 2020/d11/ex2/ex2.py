#!/usr/bin/env python

import itertools
import sys
from copy import deepcopy
from typing import Iterator, List, Tuple

Grid = List[List[str]]


def update(grid: Grid) -> Grid:
    def neightbours(x: int, y: int) -> Iterator[Tuple[int, int]]:
        for dx, dy in itertools.product(range(-1, 2), range(-1, 2)):
            if dx == 0 and dy == 0:
                continue

            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                if grid[new_x][new_y] in "L#":
                    yield new_x, new_y
                    break
                new_x, new_y = new_x + dx, new_y + dy

    new_grid = deepcopy(grid)

    for x, y in itertools.product(range(len(grid)), range(len(grid[0]))):
        num_alive = sum(grid[nx][ny] == "#" for nx, ny in neightbours(x, y))
        if num_alive == 0 and grid[x][y] == "L":
            new_grid[x][y] = "#"
        elif num_alive >= 5 and grid[x][y] == "#":
            new_grid[x][y] = "L"

    return new_grid


def solve(grid: Grid) -> int:
    while (new_grid := update(grid)) != grid:
        grid = new_grid
    return sum(sum(pos == "#" for pos in line) for line in grid)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve([[line[i] for i in range(len(line))] for line in input]))


if __name__ == "__main__":
    main()
