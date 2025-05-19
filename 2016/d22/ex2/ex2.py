#!/usr/bin/env python

import heapq
import sys
from collections.abc import Iterable
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Filesystem(NamedTuple):
    size: int
    used: int

    @property
    def avail(self) -> int:
        return self.size - self.used


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[Point, Filesystem]:
        raw_fs, raw_size, raw_used, raw_avail, _ = input.split()
        size = int(raw_size.removesuffix("T"))
        used = int(raw_used.removesuffix("T"))
        avail = int(raw_avail.removesuffix("T"))
        assert size == (used + avail)  # Sanity check
        *_, x, y = raw_fs.split("-")
        return Point(int(x[1:]), int(y[1:])), Filesystem(size, used)

    def parse(input: str) -> dict[Point, Filesystem]:
        return {node: fs for node, fs in map(parse_line, input.splitlines()[2:])}

    def neighbours(p: Point) -> Iterable[Point]:
        for dx, dy in (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ):
            yield Point(p.x + dx, p.y + dy)

    def dijkstra(start: Point, end: Point, points: set[Point]) -> int:
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
                if n not in points:
                    continue
                heapq.heappush(queue, (dist + 1, n))

        assert False  # Sanity check

    def dist(p: Point, other: Point) -> int:
        return abs(p.x - other.x) + abs(p.y - other.y)

    def has_angle(p: Point, other: Point) -> int:
        return p.x != other.x and p.y != other.y

    def data_migration(start: Point, end: Point) -> int:
        # Moving the data once is a 5 step move, unless it is on an angle, where it is 3
        # Assumes there's no wall between either points
        return 5 * dist(start, end) - 2 * has_angle(start, end)

    df = parse(input)
    # The data moves from the goal to us, hence `start` and `end` are "reversed"
    start = max(p for p in df.keys() if p.y == 0)
    end = Point(0, 0)
    # The "hole" must be used to migrate the data to us
    hole = next(p for p, fs in df.items() if fs.used == 0)
    # The "walls" are nodes which are too big to move, effectively blocking us
    walls = {p for p, fs in df.items() if fs.used > df[hole].avail}
    accessible = df.keys() - walls

    return min(
        dijkstra(hole, n, accessible) + 1 + data_migration(n, end)
        for n in neighbours(start)
        if n in accessible
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
