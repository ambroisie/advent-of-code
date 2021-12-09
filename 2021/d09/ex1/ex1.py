#!/usr/bin/env python

import itertools
import sys
from typing import Iterator, List, Tuple

HeightMap = List[List[int]]
Point = Tuple[int, int]


def solve(input: List[str]) -> int:
    height_map = [[int(c) for c in line] for line in input]

    def neighbours_of(point: Point) -> Iterator[Point]:
        for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):
            x, y = point[0] + dx, point[1] + dy
            if x < 0 or x >= len(height_map):
                continue
            if y < 0 or y >= len(height_map[0]):
                continue
            yield x, y

    def is_low_point(point: Point) -> bool:
        for neighbour in neighbours_of(point):
            if height_map[neighbour[0]][neighbour[1]] <= height_map[point[0]][point[1]]:
                return False
        return True

    def risk_level(point: Point) -> int:
        return 1 + height_map[point[0]][point[1]]

    points = [(x, y) for x in range(len(height_map)) for y in range(len(height_map[0]))]
    return sum(risk_level(p) for p in points if is_low_point(p))


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
