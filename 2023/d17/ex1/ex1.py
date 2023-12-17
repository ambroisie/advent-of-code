#!/usr/bin/env python

import functools
import heapq
import itertools
import sys
from collections.abc import Iterator
from enum import Enum
from types import NotImplementedType
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@functools.total_ordering
class Direction(Enum):
    NORTH = Point(-1, 0)
    SOUTH = Point(1, 0)
    EAST = Point(0, 1)
    WEST = Point(0, -1)

    def apply(self, pos: Point) -> Point:
        dx, dy = self.value
        return Point(pos.x + dx, pos.y + dy)

    def __le__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Direction):
            return NotImplemented
        return self.value <= other.value


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> dict[Point, int]:
        res: dict[Point, int] = {}

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                res[Point(x, y)] = int(c)

        return res

    def possible_directions(
        dir: Direction, in_a_row: int
    ) -> Iterator[tuple[Direction, int]]:
        if in_a_row < 3:
            yield dir, in_a_row + 1
        DIRECTIONS = {
            Direction.NORTH: (Direction.EAST, Direction.WEST),
            Direction.SOUTH: (Direction.EAST, Direction.WEST),
            Direction.WEST: (Direction.NORTH, Direction.SOUTH),
            Direction.EAST: (Direction.NORTH, Direction.SOUTH),
        }
        yield from zip(DIRECTIONS[dir], itertools.repeat(1))

    def minimal_path(map: dict[Point, int], start: Point, end: Point) -> int:
        class PathNode(NamedTuple):
            pos: Point
            dir: Direction
            in_a_row: int

        QueueNode = tuple[int, PathNode]

        # Start with arbitrary south direction with *0* in a row, to get correct neighbours
        queue: list[QueueNode] = [(0, PathNode(start, Direction.SOUTH, 0))]
        seen: set[PathNode] = set()

        while queue:
            dist, node = heapq.heappop(queue)
            if node.pos == end:
                return dist
            # If we've already seen that exact node before, don't look at it again
            if node in seen:
                continue
            # First time encountering those node conditions, record it
            seen.add(node)
            for dir, in_a_row in possible_directions(node.dir, node.in_a_row):
                new_pos = dir.apply(node.pos)
                if new_pos not in map:
                    continue
                new_dist = dist + map[new_pos]
                new_node = PathNode(new_pos, dir, in_a_row)
                heapq.heappush(queue, (new_dist, new_node))

        assert False  # Sanity check

    map = parse(input)
    start = Point(0, 0)
    end = Point(len(input) - 1, len(input[0]) - 1)
    return minimal_path(map, start, end)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
