#!/usr/bin/env python

import enum
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


class LevelDelta(enum.IntEnum):
    PATH = 0
    INNER_GATE = 1
    OUTER_GATE = -1


Graph = dict[Point, set[tuple[Point, LevelDelta]]]


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
        res: dict[Point, set[tuple[Point, LevelDelta]]] = defaultdict(set)

        for p in paths:
            res[p] |= {(n, LevelDelta.PATH) for n in p.neighbours() if n in paths}

        outer_x = {min(p.x for p in paths), max(p.x for p in paths)}
        outer_y = {min(p.y for p in paths), max(p.y for p in paths)}

        for gate, points in gates.items():
            if len(points) == 1:
                assert gate in ("AA", "ZZ")  # Sanity check
                continue
            for p in points:
                other = next(iter(other for other in points if other != p))
                delta = (
                    LevelDelta.OUTER_GATE
                    if p.x in outer_x or p.y in outer_y
                    else LevelDelta.INNER_GATE
                )
                res[p].add((other, delta))
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

    def dijkstra(start: Point, end: Point, graph: Graph) -> int:
        # Priority queue of (distance, point, level)
        queue = [(0, start, 0)]
        seen: set[tuple[Point, int]] = set()

        while len(queue) > 0:
            dist, p, level = heapq.heappop(queue)
            if p == end and level == 0:
                return dist
            # We must have seen p at this level with a smaller distance before
            if (p, level) in seen:
                continue
            # First time encountering p at this level, must be the smallest distance to it
            seen.add((p, level))
            # Add all neighbours to be visited
            for n, delta in graph[p]:
                n_level = level + delta
                # Don't attempt to go out when at the most outer level
                if n_level < 0:
                    continue
                heapq.heappush(queue, (dist + 1, n, n_level))

        assert False  # Sanity check

    graph, start, end = parse(input.splitlines())
    return dijkstra(start, end, graph)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
