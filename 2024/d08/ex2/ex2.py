#!/usr/bin/env python

import itertools
import sys
from collections import defaultdict
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def parse(input: list[str]) -> dict[str, set[Point]]:
        res: dict[str, set[Point]] = defaultdict(set)
        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == ".":
                    continue
                res[c].add(Point(x, y))
        return res

    def find_antinodes(grid: dict[str, set[Point]], dims: Point) -> set[Point]:
        max_x, max_y = dims
        antinodes: set[Point] = set()
        for antennas in grid.values():
            for start, end in itertools.permutations(antennas, 2):
                dx, dy = end.x - start.x, end.y - start.y
                for i in itertools.count():
                    x, y = start.x - dx * i, start.y - dy * i
                    if not (0 <= x < max_x):
                        break
                    if not (0 <= y < max_y):
                        break
                    antinodes.add(Point(x, y))
        return antinodes

    lines = input.splitlines()
    max_x, max_y = len(lines), len(lines[0])
    grid = parse(lines)
    return len(find_antinodes(grid, Point(max_x, max_y)))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
