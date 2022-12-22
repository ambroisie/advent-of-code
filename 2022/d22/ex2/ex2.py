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


class CubeFace(enum.IntEnum):
    #   A B
    #   C
    # D E
    # F
    A = enum.auto()
    B = enum.auto()
    C = enum.auto()
    D = enum.auto()
    E = enum.auto()
    F = enum.auto()

    def minmax(self) -> tuple[Point, Point]:
        match self:
            case CubeFace.A:
                return Point(1, 51), Point(50, 100)
            case CubeFace.B:
                return Point(1, 101), Point(50, 150)
            case CubeFace.C:
                return Point(51, 51), Point(100, 100)
            case CubeFace.D:
                return Point(101, 1), Point(150, 50)
            case CubeFace.E:
                return Point(101, 51), Point(150, 100)
            case CubeFace.F:
                return Point(151, 1), Point(200, 50)

    def belongs(self, p: Point) -> bool:
        (minx, miny), (maxx, maxy) = self.minmax()
        return (minx <= p.x <= maxx) and (miny <= p.y <= maxy)

    @classmethod
    def from_point(cls, p: Point) -> "CubeFace":
        return next(f for f in cls if f.belongs(p))

    def walk_along(self, p: Point, dir: Direction) -> tuple[Point, Direction]:
        assert self.belongs(p)  # Sanity check
        new_p = p + dir.to_delta()
        if self.belongs(new_p):
            return new_p, dir
        return self._do_wrap(p, dir)

    def _do_wrap(self, p: Point, dir: Direction) -> tuple[Point, Direction]:
        match (self, dir):
            case CubeFace.A, Direction.EAST:  # A -> B
                return p + dir.to_delta(), dir
            case CubeFace.A, Direction.SOUTH:  # A -> C
                return p + dir.to_delta(), dir
            case CubeFace.A, Direction.WEST:  # A -> D
                return Point(151 - p.x, 1), Direction.EAST
            case CubeFace.A, Direction.NORTH:  # A -> F
                return Point(100 + p.y, 1), Direction.EAST

            case CubeFace.B, Direction.EAST:  # B -> E
                return Point(151 - p.x, 100), Direction.WEST
            case CubeFace.B, Direction.SOUTH:  # B -> C
                return Point(p.y - 50, 100), Direction.WEST
            case CubeFace.B, Direction.WEST:  # B -> A
                return p + dir.to_delta(), dir
            case CubeFace.B, Direction.NORTH:  # B -> F
                return Point(200, p.y - 100), Direction.NORTH

            case CubeFace.C, Direction.EAST:  # C -> B
                return Point(50, p.x + 50), Direction.NORTH
            case CubeFace.C, Direction.SOUTH:  # C -> E
                return p + dir.to_delta(), dir
            case CubeFace.C, Direction.WEST:  # C -> D
                return Point(101, p.x - 50), Direction.SOUTH
            case CubeFace.C, Direction.NORTH:  # C -> A
                return p + dir.to_delta(), dir

            case CubeFace.D, Direction.EAST:  # D -> E
                return p + dir.to_delta(), dir
            case CubeFace.D, Direction.SOUTH:  # D -> F
                return p + dir.to_delta(), dir
            case CubeFace.D, Direction.WEST:  # D -> A
                return Point(151 - p.x, 51), Direction.EAST
            case CubeFace.D, Direction.NORTH:  # D -> C
                return Point(50 + p.y, 51), Direction.EAST

            case CubeFace.E, Direction.EAST:  # E -> B
                return Point(151 - p.x, 150), Direction.WEST
            case CubeFace.E, Direction.SOUTH:  # E -> F
                return Point(100 + p.y, 50), Direction.WEST
            case CubeFace.E, Direction.WEST:  # E -> D
                return p + dir.to_delta(), dir
            case CubeFace.E, Direction.NORTH:  # E -> C
                return p + dir.to_delta(), dir

            case CubeFace.F, Direction.EAST:  # F -> E
                return Point(150, p.x - 100), Direction.NORTH
            case CubeFace.F, Direction.SOUTH:  # F -> B
                return Point(1, 100 + p.y), Direction.SOUTH
            case CubeFace.F, Direction.WEST:  # F -> A
                return Point(1, p.x - 100), Direction.SOUTH
            case CubeFace.F, Direction.NORTH:  # F -> D
                return p + dir.to_delta(), dir

        assert False


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

    def points_along(start: Point, dir: Direction) -> Iterator[tuple[Point, Direction]]:
        while True:
            start, dir = CubeFace.from_point(start).walk_along(start, dir)
            yield start, dir

    assert input[-2] == ""  # Sanity check

    facing = Direction.EAST
    start, map = parse_map(input[:-2])
    instructions = parse_instruction(input[-1])

    for instr in instructions:
        if isinstance(instr, Rotation):
            facing = facing.turn(instr)
            continue
        for p, new_facing in take(instr, points_along(start, facing)):
            if map[p] == Tile.WALL:
                break
            start = p
            facing = new_facing

    return 1000 * start.x + 4 * start.y + facing


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
