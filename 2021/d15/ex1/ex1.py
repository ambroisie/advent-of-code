#!/usr/bin/env python

import heapq
import itertools
import sys
from typing import Iterator, List, NamedTuple, Set, Tuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: List[str]) -> int:
    levels = [[int(c) for c in line] for line in input]

    def neighbours(p: Point) -> Iterator[Point]:
        for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):
            x, y = p.x + dx, p.y + dy
            if x < 0 or x >= len(levels):
                continue
            if y < 0 or y >= len(levels[0]):
                continue
            yield Point(x, y)

    def djikstra(start: Point, end: Point) -> int:
        # Priority queue of (distance, point)
        queue = [(0, start)]
        seen: Set[Point] = set()

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
                heapq.heappush(queue, (dist + levels[n.x][n.y], n))

        assert False  # Sanity check

    return djikstra(Point(0, 0), Point(len(levels) - 1, len(levels[0]) - 1))


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
