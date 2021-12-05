#!/usr/bin/env python

import itertools
import sys
from collections import Counter
from typing import Iterable, List, NamedTuple, Tuple


class Point(NamedTuple):
    x: int
    y: int


Line = Tuple[Point, Point]


def solve(input: List[str]) -> int:
    def parse_line(line: str) -> Line:
        def parse_point(point: str) -> Point:
            x, y = map(int, point.split(","))
            return Point(x, y)

        p1, p2 = map(parse_point, line.split(" -> "))
        return (p1, p2)

    def line_to_points(line: Line) -> Iterable[Point]:
        def inclusive_range_any_order(a: int, b: int) -> Iterable[int]:
            if a < b:
                yield from range(a, b + 1)
            else:
                yield from range(a, b - 1, -1)

        p1, p2 = line

        xs = inclusive_range_any_order(p1.x, p2.x)
        ys = inclusive_range_any_order(p1.y, p2.y)

        if p1.x == p2.x:
            xs = itertools.repeat(p1.x)

        if p1.y == p2.y:
            ys = itertools.repeat(p1.y)

        yield from map(Point._make, zip(xs, ys))

    lines = list(map(parse_line, input))
    counts = Counter(itertools.chain.from_iterable(line_to_points(l) for l in lines))

    return sum(counts[p] > 1 for p in counts)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
