#!/usr/bin/env python

import dataclasses
import enum
import sys
from typing import NamedTuple


def sign(n: int) -> int:
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0


class Direction(enum.Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


@dataclasses.dataclass
class Move:
    dir: Direction
    len: int

    @classmethod
    def from_input(cls, line: str) -> "Move":
        d, l = line.split()
        return cls(Direction(d), int(l))


class Point(NamedTuple):
    x: int
    y: int

    def move(self, direction: Direction) -> "Point":
        match direction:
            case Direction.UP:
                dx, dy = 1, 0
            case Direction.DOWN:
                dx, dy = -1, 0
            case Direction.LEFT:
                dx, dy = 0, -1
            case Direction.RIGHT:
                dx, dy = 0, 1
        return Point(self.x + dx, self.y + dy)


@dataclasses.dataclass
class Rope:
    points: list[Point] = dataclasses.field(init=False)
    _tail_positions: set[Point] = dataclasses.field(init=False)

    def __init__(self, *, length: int = 2) -> None:
        assert length > 0
        self.points = [Point(0, 0)] * length
        self._tail_positions = {self.points[-1]}

    def move(self, move: Move) -> None:
        for _ in range(move.len):
            self.points[0] = self.points[0].move(move.dir)
            for i in range(1, len(self.points)):
                self.points[i] = self.__move_tail(self.points[i - 1], self.points[i])
            self._tail_positions.add(self.points[-1])

    @staticmethod
    def __move_tail(head: Point, tail: Point) -> Point:
        delta_x, delta_y = head.x - tail.x, head.y - tail.y

        if abs(delta_x) <= 1 and abs(delta_y) <= 1:
            return tail

        dx, dy = sign(delta_x), sign(delta_y)
        return Point(tail.x + dx, tail.y + dy)


def solve(input: list[str]) -> int:
    moves = map(Move.from_input, input)
    rope = Rope(length=2)

    for move in moves:
        rope.move(move)

    return len(rope._tail_positions)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
