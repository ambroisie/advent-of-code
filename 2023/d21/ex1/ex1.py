#!/usr/bin/env python

import sys
from collections import defaultdict, deque
from typing import NamedTuple, Optional


class Point(NamedTuple):
    x: int
    y: int


GardenPoints = set[Point]


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> tuple[GardenPoints, Point]:
        start: Optional[Point] = None
        points: GardenPoints = set()

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == "#":
                    continue
                if c == "S":
                    start = Point(x, y)
                points.add(Point(x, y))

        assert start is not None  # Sanity check
        return points, start

    def explore(points: GardenPoints, start: Point) -> dict[Point, int]:
        res: dict[Point, int] = {}
        queue: deque[tuple[Point, int]] = deque([(start, 0)])

        while queue:
            point, dist = queue.popleft()
            # If we already saw the point, then we saw it at a smaller distance
            if point in res:
                continue
            # If it's not an actual garden point (rocks, out-of-bounds), don't log it
            if point not in points:
                continue
            res[point] = dist
            for dx, dy in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ):
                queue.append((Point(point.x + dx, point.y + dy), dist + 1))

        return res

    def reachable_in(distances: dict[Point, int], steps: int) -> set[Point]:
        inverse_dist: dict[int, list[Point]] = defaultdict(list)
        for p, dist in distances.items():
            inverse_dist[dist].append(p)

        return set(p for i in range(steps % 2, steps + 1, 2) for p in inverse_dist[i])

    points, start = parse(input)
    distances = explore(points, start)
    return len(reachable_in(distances, 64))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
