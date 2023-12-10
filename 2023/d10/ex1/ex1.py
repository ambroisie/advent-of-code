#!/usr/bin/env python

import sys
from collections.abc import Iterator
from enum import Enum, StrEnum
from typing import NamedTuple, Optional


class Point(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    NORTH = Point(-1, 0)
    SOUTH = Point(1, 0)
    WEST = Point(0, -1)
    EAST = Point(0, 1)

    def apply(self, pos: "Point") -> "Point":
        dx, dy = self.value
        return Point(pos.x + dx, pos.y + dy)


class Pipe(StrEnum):
    VERTICAL = "|"
    HORIZONTAL = "-"
    NE_BEND = "L"
    NW_BEND = "J"
    SW_BEND = "7"
    SE_BEND = "F"

    @classmethod
    def from_connection(cls, connections: dict[Direction, bool]) -> "Pipe":
        assert sum(connections.values()) == 2  # Sanity check
        if connections.get(Direction.NORTH, False):
            if connections.get(Direction.SOUTH, False):
                return cls.VERTICAL
            if connections.get(Direction.EAST, False):
                return cls.NE_BEND
            if connections.get(Direction.WEST, False):
                return cls.NW_BEND
        if connections.get(Direction.SOUTH, False):
            if connections.get(Direction.WEST, False):
                return cls.SW_BEND
            if connections.get(Direction.EAST, False):
                return cls.SE_BEND
        assert connections[Direction.WEST] and connections[Direction.EAST]
        return cls.HORIZONTAL

    def neighbours(self, pos: Point) -> Iterator[Point]:
        deltas: tuple[Direction, Direction]

        match self:
            case self.VERTICAL:
                deltas = (Direction.NORTH, Direction.SOUTH)
            case self.HORIZONTAL:
                deltas = (Direction.WEST, Direction.EAST)
            case self.NE_BEND:
                deltas = (Direction.NORTH, Direction.EAST)
            case self.NW_BEND:
                deltas = (Direction.NORTH, Direction.WEST)
            case self.SW_BEND:
                deltas = (Direction.SOUTH, Direction.WEST)
            case self.SE_BEND:
                deltas = (Direction.SOUTH, Direction.EAST)

        for dir in deltas:
            yield dir.apply(pos)

    def go_through(self, pos: Point, prev: Point) -> Point:
        for dest in self.neighbours(pos):
            if dest == prev:
                continue
            return dest
        assert False  # Sanity check


Pipes = dict[Point, Pipe]


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> tuple[Point, Pipes]:
        start: Optional[Point] = None
        pipes: Pipes = {}

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == ".":
                    continue
                if c == "S":
                    start = Point(x, y)
                    continue
                pipes[Point(x, y)] = Pipe(c)

        assert start is not None  # Sanity check
        return start, pipes

    def iter_pipe(cur: Point, start: Point, pipes: Pipes) -> Iterator[Point]:
        prev = start
        while True:
            if cur == start:
                break
            if cur not in pipes:
                break
            # Check that the receiving pipe is connected to previous one
            if prev not in pipes[cur].neighbours(cur):
                return
            yield cur
            cur, prev = pipes[cur].go_through(cur, prev), cur
        # Yield the loop element
        if cur == start:
            yield cur

    # Return the possible pipes that start can be
    def resolve_start(start: Point, pipes: Pipes) -> Pipe:
        # Returns the direction which closes the loop, if there is one
        def explore(dir: Direction) -> Optional[Direction]:
            points = list(iter_pipe(dir.apply(start), start, pipes))
            if len(points) == 0:
                return None
            penultimate, last = points[-2], points[-1]
            if last != start:
                return None
            return Direction(Point(penultimate.x - last.x, penultimate.y - last.y))

        res: set[Pipe] = set()
        for dir in Direction:
            if (resulting_dir := explore(dir)) is None:
                continue
            res.add(Pipe.from_connection({dir: True, resulting_dir: True}))
        assert len(res) == 1  # Instructions say there is exactly one loop
        return res.pop()

    def compute_dist(start: Point, pipes: Pipes) -> dict[Point, int]:
        res = {start: 0}

        for n in pipes[start].neighbours(start):
            for d, p in enumerate(iter_pipe(n, start, pipes), start=1):
                res[p] = min(d, res.get(p, d))

        return res

    start, pipes = parse(input)
    pipes[start] = resolve_start(start, pipes)
    return max(compute_dist(start, pipes).values())


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
