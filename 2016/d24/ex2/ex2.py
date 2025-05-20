#!/usr/bin/env python

import collections
import heapq
import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def parse(input: str) -> tuple[set[Point], dict[int, Point]]:
        spaces: set[Point] = set()
        waypoints: dict[int, Point] = {}
        for x, line in enumerate(input.splitlines()):
            for y, c in enumerate(line):
                if c == "#":
                    continue
                p = Point(x, y)
                spaces.add(p)
                if c != ".":
                    waypoints[int(c)] = p
        return spaces, waypoints

    def neighbours(p: Point) -> Iterator[Point]:
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

    def waypoint_distances(
        points: set[Point], waypoints: dict[int, Point]
    ) -> dict[int, dict[int, int]]:
        res: dict[int, dict[int, int]] = collections.defaultdict(dict)
        for p1, p2 in itertools.combinations(waypoints.keys(), 2):
            dist = dijkstra(waypoints[p1], waypoints[p2], points)
            res[p1][p2] = dist
            res[p2][p1] = dist
        return res

    def traveling_salesman(
        start: int,
        points: set[Point],
        waypoints: dict[int, Point],
    ) -> int:
        def list_travel_loops() -> Iterator[Iterator[int]]:
            for destinations in itertools.permutations(waypoints.keys() - {start}):
                yield itertools.chain([start], destinations, [start])

        distances = waypoint_distances(points, waypoints)
        return min(
            sum(distances[s][e] for s, e in itertools.pairwise(travel_plan))
            for travel_plan in list_travel_loops()
        )

    points, waypoints = parse(input)
    return traveling_salesman(0, points, waypoints)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
