#!/usr/bin/env python

import collections
import copy
import enum
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.StrEnum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"

    def apply(self, p: Point) -> Point:
        delta: Point
        match self:
            case Direction.NORTH:
                delta = Point(-1, 0)
            case Direction.SOUTH:
                delta = Point(1, 0)
            case Direction.WEST:
                delta = Point(0, -1)
            case Direction.EAST:
                delta = Point(0, 1)
        return Point(p.x + delta.x, p.y + delta.y)


START = Point(0, 0)


def solve(input: str) -> int:
    def to_graph(regex: str) -> dict[Point, set[Point]]:
        res: dict[Point, set[Point]] = collections.defaultdict(set)
        stack: list[set[Point]] = [{START}]
        current_branches: set[Point] = set()
        for c in regex.removeprefix("^").removesuffix("$"):
            if c == "(":
                stack.append(copy.deepcopy(stack[-1]))
                current_branches = set()
            elif c == "|":
                current_branches |= stack.pop()
                stack.append(copy.deepcopy(stack[-1]))
            elif c == ")":
                current_branches |= stack.pop()
                stack[-1] = current_branches
            else:
                dir = Direction(c)
                for p in stack[-1]:
                    neighbour = dir.apply(p)
                    res[p].add(neighbour)
                    res[neighbour].add(p)
                stack[-1] = {dir.apply(p) for p in stack[-1]}

        return dict(res)

    def start_distances(graph: dict[Point, set[Point]]) -> dict[Point, int]:
        queue = collections.deque([(0, START)])
        distances: dict[Point, int] = {}

        while queue:
            dist, p = queue.popleft()
            if p in distances:
                continue
            distances[p] = dist
            for n in graph.get(p, set()):
                queue.append((dist + 1, n))

        return distances

    # Remove the anchors, we don't use them in the parsing code
    graph = to_graph(input.strip())
    distances = start_distances(graph)
    return sum(d >= 1000 for d in distances.values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
