#!/usr/bin/env python

import enum
import itertools
import sys
from typing import Iterable, Iterator, List, NamedTuple, Set


class Point(NamedTuple):
    x: int
    y: int


class Map(NamedTuple):
    east: Set[Point]
    south: Set[Point]
    dimensions: Point


def solve(input: List[str]) -> int:
    def parse() -> Map:
        east, south = set(), set()

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == ".":
                    continue
                if c == "v":
                    south.add(Point(x, y))
                if c == ">":
                    east.add(Point(x, y))

        return Map(east, south, Point(len(input), len(input[0])))

    def step(sea_cucumbers: Map) -> Map:
        def move_east(p: Point) -> Point:
            return Point(p.x, (p.y + 1) % sea_cucumbers.dimensions.y)

        def move_south(p: Point) -> Point:
            return Point((p.x + 1) % sea_cucumbers.dimensions.x, p.y)

        east, south = set(), set()

        for old_p in sea_cucumbers.east:
            p = move_east(old_p)
            if p in sea_cucumbers.east or p in sea_cucumbers.south:
                east.add(old_p)
                continue
            east.add(p)

        for old_p in sea_cucumbers.south:
            p = move_south(old_p)
            if p in east or p in sea_cucumbers.south:
                south.add(old_p)
                continue
            south.add(p)

        return Map(east, south, sea_cucumbers.dimensions)

    def debug(map: Map) -> None:
        for x in range(map.dimensions.x):
            print(
                "".join(
                    (
                        "v"
                        if Point(x, y) in map.south
                        else ">" if Point(x, y) in map.east else "."
                    )
                    for y in range(map.dimensions.y)
                )
            )

    sea_cucumbers = parse()
    for i in itertools.count(1):
        if (new_map := step(sea_cucumbers)) == sea_cucumbers:
            return i
        print(i)
        sea_cucumbers = new_map

    assert False  # Sanity check


def main() -> None:
    input = [line.rstrip("\n") for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
