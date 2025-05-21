#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def parse(input: str) -> set[Point]:
        return {
            Point(x, y)
            for x, line in enumerate(input.splitlines())
            for y, c in enumerate(line)
            if c == "#"
        }

    def neighbours(p: Point) -> Iterator[Point]:
        for dx, dy in itertools.product((-1, 0, 1), repeat=2):
            if dx == 0 and dy == 0:
                continue
            yield Point(p.x + dx, p.y + dy)

    def step(lights: set[Point], dimensions: Point) -> set[Point]:
        res: set[Point] = set()
        for p in map(
            Point._make,
            itertools.product(range(dimensions.x), range(dimensions.y)),
        ):
            num_alive = sum(n in lights for n in neighbours(p))
            if p in lights and num_alive not in (2, 3):
                continue
            if p not in lights and num_alive != 3:
                continue
            res.add(p)

        return res

    lights = parse(input)
    dimensions = Point(100, 100)
    for _ in range(100):
        lights = step(lights, dimensions)
    return len(lights)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
