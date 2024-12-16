#!/usr/bin/env python

import enum
import heapq
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class ParsedMaze(NamedTuple):
    start: Point
    end: Point
    blocks: set[Point]


class Direction(enum.IntEnum):
    EAST = enum.auto()
    WEST = enum.auto()
    NORTH = enum.auto()
    SOUTH = enum.auto()

    def rotations(self) -> tuple["Direction", "Direction"]:
        match self:
            case Direction.EAST | Direction.WEST:
                return (Direction.NORTH, Direction.SOUTH)
            case Direction.NORTH | Direction.SOUTH:
                return (Direction.EAST, Direction.WEST)

    def step(self, p: Point) -> Point:
        dx: int
        dy: int

        match self:
            case Direction.EAST:
                dx, dy = 0, 1
            case Direction.WEST:
                dx, dy = 0, -1
            case Direction.NORTH:
                dx, dy = -1, 0
            case Direction.SOUTH:
                dx, dy = 1, 0

        return Point(p.x + dx, p.y + dy)


Node = tuple[Point, Direction]


def solve(input: str) -> int:
    def parse(input: list[str]) -> ParsedMaze:
        start: Point | None = None
        end: Point | None = None
        blocks: set[Point] = set()
        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == ".":
                    continue
                p = Point(x, y)
                if c == "S":
                    start = p
                elif c == "E":
                    end = p
                elif c == "#":
                    blocks.add(p)
                else:
                    assert False  # Sanity check
        assert start is not None  # Sanity check
        assert end is not None  # Sanity check
        return ParsedMaze(start, end, blocks)

    def djikstra(start: Point, end: Point, blocks: set[Point]) -> int:
        def next_moves(
            pos: Point,
            dir: Direction,
        ) -> Iterator[tuple[int, Point, Direction]]:
            transitions = [(1, dir.step(pos), dir)]
            for new_dir in dir.rotations():
                transitions.append((1000, pos, new_dir))
            for cost, pos, dir in transitions:
                if pos in blocks:
                    continue
                yield cost, pos, dir

        # Priority queue of (distance, point, direction)
        queue = [(0, start, Direction.EAST)]
        seen: set[Node] = set()

        while len(queue) > 0:
            cost, p, dir = heapq.heappop(queue)
            if p == end:
                return cost
            # We must have seen (p, dir) with a smaller distance before
            if (p, dir) in seen:
                continue
            # First time encountering (p, dir), must be the smallest distance to it
            seen.add((p, dir))
            # Add all neighbours to be visited
            for n_cost, n, n_dir in next_moves(p, dir):
                heapq.heappush(queue, (cost + n_cost, n, n_dir))

        assert False  # Sanity check

    start, end, blocks = parse(input.splitlines())
    return djikstra(start, end, blocks)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
