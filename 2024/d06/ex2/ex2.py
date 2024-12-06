#!/usr/bin/env python

import enum
import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.StrEnum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

    def step(self, p: Point) -> Point:
        dx: int
        dy: int

        match self:
            case Direction.UP:
                dx, dy = -1, 0
            case Direction.RIGHT:
                dx, dy = 0, 1
            case Direction.DOWN:
                dx, dy = 1, 0
            case Direction.LEFT:
                dx, dy = 0, -1

        return Point(p.x + dx, p.y + dy)

    def turn_right(self) -> "Direction":
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP


class Guard(NamedTuple):
    pos: Point
    dir: Direction

    def patrol_step(self, blockers: set[Point]) -> "Guard":
        next_step = self.dir.step(self.pos)
        if next_step not in blockers:
            return Guard(next_step, self.dir)
        return Guard(self.pos, self.dir.turn_right())


def solve(input: str) -> int:
    def parse(input: list[str]) -> tuple[Guard, set[Point]]:
        guard: Guard | None = None
        blockers: set[Point] = set()

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == ".":
                    continue
                if c == "#":
                    blockers.add(Point(x, y))
                    continue
                guard = Guard(Point(x, y), Direction(c))

        assert guard is not None  # Sanity check
        return guard, blockers

    def loops(guard: Guard, blockers: set[Point], dims: Point) -> int:
        max_x, max_y = dims
        visited: set[Guard] = set()
        while True:
            if not (0 <= guard.pos.x < max_x):
                break
            if not (0 <= guard.pos.y < max_y):
                break
            if guard in visited:
                return True
            visited.add(guard)
            guard = guard.patrol_step(blockers)
        return False

    def count_obstructions(guard: Guard, blockers: set[Point], dims: Point) -> int:
        res = 0
        max_x, max_y = dims
        for x, y in itertools.product(range(max_x), range(max_y)):
            candidate = Point(x, y)
            if candidate in blockers:
                continue
            if candidate == guard.pos:
                continue
            if not loops(guard, blockers | {candidate}, dims):
                continue
            res += 1
        return res

    lines = input.splitlines()
    guard, blockers = parse(lines)
    max_x, max_y = len(lines), len(lines[0])
    return count_obstructions(guard, blockers, Point(max_x, max_y))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
