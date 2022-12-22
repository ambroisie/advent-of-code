#!/usr/bin/env python

import enum
import itertools
import sys
from collections.abc import Iterable, Iterator
from typing import NamedTuple, TypeVar, Union

T = TypeVar("T")


def take(n: int, iterable: Iterable[T]) -> Iterator[T]:
    return itertools.islice(iterable, n)


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)


class Tile(str, enum.Enum):
    AIR = "."
    WALL = "#"


class Direction(enum.IntEnum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def turn(self, rot: "Rotation") -> "Direction":
        if rot == Rotation.LEFT:
            return Direction((self - 1 + 4) % 4)
        if rot == Rotation.RIGHT:
            return Direction((self + 1) % 4)
        assert False  # Sanity check

    def to_delta(self) -> Point:
        match self:
            case Direction.NORTH:
                return Point(-1, 0)
            case Direction.SOUTH:
                return Point(1, 0)
            case Direction.EAST:
                return Point(0, 1)
            case Direction.WEST:
                return Point(0, -1)


class Rotation(str, enum.Enum):
    LEFT = "L"
    RIGHT = "R"


Map = dict[Point, Tile]


def solve(input: list[str]) -> int:
    def parse_map(input: list[str]) -> tuple[Point, Map]:
        res: Map = {}

        for i, line in enumerate(input, start=1):
            for j, c in enumerate(line, start=1):
                if c == " ":
                    continue
                res[Point(i, j)] = Tile(c)

        return min(p for p in res.keys()), res

    def parse_instruction(input: str) -> list[Union[Rotation, int]]:
        res: list[Union[Rotation, int]] = []
        i = 0
        while i < len(input):
            # Parse direction
            if input[i] in list(Rotation):
                res.append(Rotation(input[i]))
                i += 1
                continue
            # Parse int
            j = i + 1
            while j < len(input) and input[j] not in list(Rotation):
                j += 1
            res.append(int(input[i:j]))
            i = j

        return res

    def points_along(start: Point, map: Map, dir: Direction) -> Iterator[Point]:
        delta = dir.to_delta()
        while True:
            start = start + delta
            # Wrap around if about to go out-of-bounds
            if start not in map:
                while (new_start := start - delta) in map:
                    start = new_start
            yield start

    assert input[-2] == ""  # Sanity check

    facing = Direction.EAST
    start, map = parse_map(input[:-2])
    instructions = parse_instruction(input[-1])

    for instr in instructions:
        if isinstance(instr, Rotation):
            facing = facing.turn(instr)
            continue
        for p in take(instr, points_along(start, map, facing)):
            if map[p] == Tile.WALL:
                break
            start = p

    return 1000 * start.x + 4 * start.y + facing


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
