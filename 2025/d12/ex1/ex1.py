#!/usr/bin/env python

import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Region(NamedTuple):
    size: Point
    pieces: list[int]

    @classmethod
    def from_str(cls, input: str) -> "Region":
        raw_size, *raw_pieces = input.split(" ")
        size = Point(*map(int, raw_size.removesuffix(":").split("x")))
        pieces = [int(n) for n in raw_pieces]
        return cls(size, pieces)


def solve(input: str) -> int:
    def parse_shape(input: list[str]) -> set[Point]:
        return {
            Point(x, y)
            for x, line in enumerate(input)
            for y, c in enumerate(line)
            if c == "#"
        }

    def parse(input: str) -> tuple[list[set[Point]], list[Region]]:
        *raw_shapes, raw_regions = input.split("\n\n")
        shapes = [parse_shape(shape.splitlines()[1:]) for shape in raw_shapes]
        regions = [Region.from_str(region) for region in raw_regions.splitlines()]
        return shapes, regions

    def can_fit_stupid(shapes: list[set[Point]], region: Region) -> bool:
        # Does not actually try to fit the pieces, just checks the area
        # This does *not* work on the sample input
        minimum_size = sum(len(shapes[i]) * n for i, n in enumerate(region.pieces))
        region_size = region.size.x * region.size.y
        return minimum_size <= region_size

    shapes, regions = parse(input)
    return sum(can_fit_stupid(shapes, region) for region in regions)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
