#!/usr/bin/env python

import dataclasses
import heapq
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclasses.dataclass
class HeightMap:
    heights: list[list[int]]
    start: Point
    end: Point

    def reachable_neighbours(self, p: Point) -> Iterator[Point]:
        reachable_height = self.heights[p.x][p.y] + 1
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x, y = p.x + dx, p.y + dy
            if x < 0 or x >= len(self.heights):
                continue
            if y < 0 or y >= len(self.heights[0]):
                continue
            if self.heights[x][y] > reachable_height:
                continue
            yield Point(x, y)


def solve(input: list[str]) -> int:
    def to_height_map(input: list[str]) -> HeightMap:
        start, end = None, None
        heights = [[0 for _ in range(len(input[0]))] for _ in range(len(input))]

        for i, line in enumerate(input):
            for j, c in enumerate(line):
                height = ord(c)
                if c == "S":
                    height = ord("a")
                    start = Point(i, j)
                if c == "E":
                    height = ord("z")
                    end = Point(i, j)
                heights[i][j] = height - ord("a")

        assert start is not None  # Sanity check
        assert end is not None  # Sanity check
        return HeightMap(heights, start, end)

    def dijkstra(map: HeightMap) -> int:
        # Priority queue of (distance, point)
        queue = [(0, map.start)]
        seen: set[Point] = set()

        while len(queue) > 0:
            dist, p = heapq.heappop(queue)
            if p == map.end:
                return dist
            # We must have seen p with a smaller distance before
            if p in seen:
                continue
            # First time encountering p, must be the smallest distance to it
            seen.add(p)
            # Add all neighbours to be visited
            for n in map.reachable_neighbours(p):
                heapq.heappush(queue, (dist + 1, n))

        assert False  # Sanity check

    map = to_height_map(input)
    return dijkstra(map)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
