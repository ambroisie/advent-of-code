#!/usr/bin/env python

import enum
import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.Enum):
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)

    def apply(self, p: Point) -> Point:
        dx, dy = self.value
        return Point(p.x + dx, p.y + dy)


def solve(input: str) -> int:
    def parse_range(input: str) -> range:
        if ".." not in input:
            input = input + ".." + input
        start, end = map(int, input.split(".."))
        return range(start, end + 1)

    def parse_line(input: str) -> Iterator[Point]:
        xs, ys = sorted(input.split(", "))
        yield from map(
            Point._make,
            itertools.product(parse_range(xs[2:]), parse_range(ys[2:])),
        )

    def parse(input: list[str]) -> set[Point]:
        return {p for line in input for p in parse_line(line)}

    def flow(clay: set[Point], source: Point) -> set[Point]:
        max_y = max(p.y for p in clay)

        def helper(
            source: Point,
            water: set[Point],
            settled: set[Point],
            direction: Direction = Direction.DOWN,
        ) -> bool:
            # Clay is considered "settled"
            if source in clay:
                return True

            # We've already seen this, return early
            if source in water:
                return source in settled

            # Account for this new source
            water.add(source)

            below = Direction.DOWN.apply(source)
            if below not in clay:
                if below.y <= max_y:
                    helper(below, water, settled)
                if below not in settled:
                    return False

            left = Direction.LEFT.apply(source)
            right = Direction.RIGHT.apply(source)
            l_filled = helper(left, water, settled, Direction.LEFT)
            r_filled = helper(right, water, settled, Direction.RIGHT)

            if direction == Direction.DOWN and l_filled and r_filled:
                settled.add(source)
                while left in water:
                    settled.add(left)
                    left = Direction.LEFT.apply(left)
                while right in water:
                    settled.add(right)
                    right = Direction.RIGHT.apply(right)
                return True

            return (direction == Direction.LEFT and l_filled) or (
                direction == Direction.RIGHT and r_filled
            )

        assert source not in clay  # Sanity check
        water: set[Point] = set()
        settled: set[Point] = set()
        helper(source, water, settled)
        assert settled <= water  # Sanity check
        return settled

    clay = parse(input.splitlines())
    sys.setrecursionlimit(5000)  # HACK
    settled = flow(clay, Point(500, 0))
    return len(settled)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
