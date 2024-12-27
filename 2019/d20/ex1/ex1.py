#!/usr/bin/env python

import heapq
import sys
from collections import defaultdict
from typing import Iterator, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def neighbours(self) -> Iterator["Point"]:
        for dx, dy in (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ):
            yield Point(self.x + dx, self.y + dy)


Graph = dict[Point, set[Point]]


def solve(input: str) -> int:
    def post_process_gates(
        letters: dict[Point, str], paths: set[Point]
    ) -> dict[str, set[Point]]:
        res: dict[str, set[Point]] = defaultdict(set)
        for p1, first in letters.items():
            for dx, dy in ((0, 1), (1, 0)):
                p2 = Point(p1.x + dx, p1.y + dy)
                if p2 not in letters:
                    continue
                gate = first + letters[p2]
                p0 = Point(p1.x - dx, p1.y - dy)
                p3 = Point(p2.x + dx, p2.y + dy)
                res[gate] |= {p0, p3} & paths
        return res

    def to_graph(paths: set[Point], gates: dict[str, set[Point]]) -> Graph:
        res: dict[Point, set[Point]] = defaultdict(set)

        for p in paths:
            res[p] |= set(p.neighbours()) & paths

        for gate, points in gates.items():
            if len(points) == 1:
                assert gate in ("AA", "ZZ")  # Sanity check
                continue
            for p in points:
                res[p] |= points
                res[p].remove(p)

        return res

    def parse(input: list[str]) -> tuple[Graph, Point, Point]:
        letters: dict[Point, str] = {}
        paths: set[Point] = set()

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == "#" or c == " ":
                    continue
                p = Point(x, y)
                if c == ".":
                    paths.add(p)
                    continue
                letters[p] = c

        gates = post_process_gates(letters, paths)
        graph = to_graph(paths, post_process_gates(letters, paths))
        return graph, next(iter(gates["AA"])), next(iter(gates["ZZ"]))

    def djikstra(start: Point, end: Point, graph: Graph) -> int:
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
            for n in graph[p]:
                heapq.heappush(queue, (dist + 1, n))

        assert False  # Sanity check

    graph, start, end = parse(input.splitlines())
    return djikstra(start, end, graph)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
