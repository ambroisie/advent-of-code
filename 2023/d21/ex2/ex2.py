#!/usr/bin/env python

import sys
from typing import Iterator, NamedTuple, Optional


class Point(NamedTuple):
    x: int
    y: int


GardenPoints = set[Point]

GRID_SIZE = 131
MID_GRID = 65
STEPS = 26501365


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> tuple[GardenPoints, Point]:
        start: Optional[Point] = None
        points: GardenPoints = set()

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == "#":
                    continue
                if c == "S":
                    start = Point(x, y)
                points.add(Point(x, y))

        assert start is not None  # Sanity check
        return points, start

    def step(points: GardenPoints, positions: set[Point]) -> set[Point]:
        res: set[Point] = set()

        for p in positions:
            for dx, dy in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ):
                x = p.x + dx
                y = p.y + dy
                # Check if the *wrapped* point is part of the garden
                px = (x + GRID_SIZE) % GRID_SIZE
                py = (y + GRID_SIZE) % GRID_SIZE
                if Point(px, py) not in points:
                    continue
                res.add(Point(x, y))

        return res

    def compute_quadratic(points: GardenPoints, start: Point) -> int:
        def iterate() -> Iterator[int]:
            positions = {start}
            while True:
                yield len(positions)
                positions = step(points, positions)

        values: list[tuple[int, int]] = []
        for i, num in enumerate(iterate()):
            if i % GRID_SIZE != MID_GRID:
                continue
            values.append((i, num))
            if len(values) == 3:
                break

        # Lagrange interpolation
        (x1, y1), (x2, y2), (x3, y3) = values
        x = STEPS
        return (
            0
            # Use integer division as it happens to work in our case
            + ((x - x2) * (x - x3)) * y1 // ((x1 - x2) * (x1 - x3))
            + ((x - x1) * (x - x3)) * y2 // ((x2 - x1) * (x2 - x3))
            + ((x - x1) * (x - x2)) * y3 // ((x3 - x1) * (x3 - x2))
        )

    assert len(input) == GRID_SIZE  # Sanity check
    assert len(input[0]) == GRID_SIZE  # Sanity check
    points, start = parse(input)
    assert start == Point(MID_GRID, MID_GRID)  # Sanity check
    return compute_quadratic(points, start)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
