#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def neighbours(self) -> Iterator["Point"]:
        for dx, dy in itertools.product((-1, 0, 1), repeat=2):
            if dx == 0 and dy == 0:
                continue
            yield Point(self.x + dx, self.y + dy)


def solve(input: str) -> int:
    def spiral() -> Iterator[Point]:
        yield Point(0, 0)
        for dist in itertools.count(1):
            side = dist * 2 + 1
            for start, dx, dy in (
                (Point(dist, -dist), 0, 1),
                (Point(dist, dist), -1, 0),
                (Point(-dist, dist), 0, -1),
                (Point(-dist, -dist), 1, 0),
            ):
                # We need a non-zero step for `range`, and to make it inclusive
                stepx = dx if dx != 0 else 1
                stepy = dy if dy != 0 else 1
                # Don't include the corner, which was already output in previous loop
                # Hence, `side - 1` points in the range
                xs = range(start.x + dx, start.x + (side - 1) * dx + stepx, stepx)
                ys = range(start.y + dy, start.y + (side - 1) * dy + stepy, stepy)
                yield from (Point(x, y) for x, y in itertools.product(xs, ys))

    target = int(input)
    values = {Point(0, 0): 1}
    # Skip the origin, which we already know
    for p in itertools.islice(spiral(), 1, None):
        if (res := sum(values.get(n, 0) for n in p.neighbours())) > target:
            return res
        values[p] = res
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
