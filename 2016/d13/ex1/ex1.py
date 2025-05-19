#!/usr/bin/env python

import functools
import heapq
import sys
from collections.abc import Callable, Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def office_location_open(p: Point, number: int) -> bool:
        x, y = p
        return (x * x + 3 * x + 2 * x * y + y + y * y + number).bit_count() % 2 == 0

    def office_neighbours(p: Point, number: int) -> Iterator[Point]:
        for dx, dy in (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ):
            n = Point(p.x + dx, p.y + dy)
            if n.x < 0 or n.y < 0:
                continue
            if office_location_open(n, number):
                yield n

    def dijkstra(
        start: Point,
        end: Point,
        neighbours: Callable[[Point], Iterator[Point]],
    ) -> int:
        # Priority queue of (distance, point)
        queue = [(0, start)]
        seen: set[Point] = set()

        while len(queue) > 0:
            dist, p = heapq.heappop(queue)
            if p == end:
                return dist
            # We must have seen p with a smaller distance before
            if p in seen:
                continue
            # First time encountering p, must be the smallest distance to it
            seen.add(p)
            # Add all neighbours to be visited
            for n in neighbours(p):
                heapq.heappush(queue, (dist + 1, n))

        assert False  # Sanity check

    favorite_number = int(input.strip())
    neighbours = functools.partial(office_neighbours, number=favorite_number)
    return dijkstra(Point(1, 1), Point(31, 39), neighbours)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
