#!/usr/bin/env python

import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def parse(input: list[str]) -> dict[Point, str]:
        return {
            Point(x, y): c for x, line in enumerate(input) for y, c in enumerate(line)
        }

    def count_xmas(grid: dict[Point, str], dims: Point) -> int:
        max_x, max_y = dims
        count = 0
        for x, y in itertools.product(range(max_x), range(max_y)):
            for dx, dy in itertools.product(range(-1, 1 + 1), repeat=2):
                if dx == 0 and dy == 0:
                    continue
                count += all(
                    grid.get(Point(x + dx * i, y + dy * i)) == c
                    for i, c in enumerate("XMAS")
                )
        return count

    lines = input.splitlines()
    grid = parse(lines)
    return count_xmas(grid, Point(len(lines), len(lines[0])))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
