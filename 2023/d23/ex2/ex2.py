#!/usr/bin/env python

import copy
import sys
from collections.abc import Iterator
from typing import NamedTuple, Optional


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


Trails = set[Point]
Graph = dict[Point, dict[Point, int]]


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> Trails:
        res: Trails = set()

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == "#":
                    continue
                res.add(Point(x, y))

        return res

    def to_graph(trails: Trails) -> Graph:
        graph: Graph = {p: {} for p in trails}

        for p in trails:
            for n in p.neighbours():
                if n not in trails:
                    continue
                graph[p][n] = 1

        return graph

    # Remove every node which has exactly two neighbours (i.e: straight lines)
    def condense_graph(graph: Graph) -> Graph:
        graph = copy.deepcopy(graph)
        nodes = list(graph.keys())

        for n in nodes:
            if len(graph[n]) != 2:
                continue
            (n1, d1), (n2, d2) = graph[n].items()
            del graph[n1][n]
            del graph[n2][n]
            del graph[n]
            graph[n1][n2] = d1 + d2
            graph[n2][n1] = d1 + d2

        return graph

    def explore(graph: Graph, start: Point, end: Point) -> int:
        def recurse(start: Point, seen: set[Point]) -> Optional[int]:
            if start == end:
                return 0
            if start not in graph:
                return None
            next_step = (
                (dist, recurse(n, seen | {n}))
                for n, dist in graph[start].items()
                if n not in seen
            )
            distances = [
                (dist + steps) for dist, steps in next_step if steps is not None
            ]
            if not distances:
                return None
            return max(distances)

        res = recurse(start, {start})
        assert res is not None  # Sanity check
        return res

    trails = parse(input)
    graph = to_graph(trails)
    graph = condense_graph(graph)
    start, dest = Point(0, 1), Point(len(input) - 1, len(input[0]) - 2)
    assert start in graph  # Sanity check
    assert dest in graph  # Sanity check
    return explore(graph, start, dest)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
