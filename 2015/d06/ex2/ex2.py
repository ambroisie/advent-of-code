#!/usr/bin/env python

import collections
import enum
import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Op(enum.StrEnum):
    TURN_ON = "on"
    TOGGLE = "toggle"
    TURN_OFF = "off"


class Instruction(NamedTuple):
    op: Op
    a: Point
    b: Point

    @classmethod
    def from_str(cls, input: str) -> "Instruction":
        split_input = input.split()
        raw_a, raw_b = split_input[-3], split_input[-1]
        op = Op(split_input[1]) if split_input[0] == "turn" else Op(split_input[0])
        return Instruction(
            op,
            Point(*map(int, raw_a.split(","))),
            Point(*map(int, raw_b.split(","))),
        )

    def apply(self, screen: collections.Counter[Point]) -> collections.Counter[Point]:
        points = collections.Counter(
            Point(x, y)
            for x, y in itertools.product(
                range(self.a.x, self.b.x + 1),
                range(self.a.y, self.b.y + 1),
            )
        )
        match self.op:
            case Op.TURN_ON:
                return screen + points
            case Op.TOGGLE:
                return screen + points + points
            case Op.TURN_OFF:
                return screen - points


def solve(input: str) -> int:
    def parse(input: str) -> list[Instruction]:
        return [Instruction.from_str(line) for line in input.splitlines()]

    instructions = parse(input)
    screen: collections.Counter[Point] = collections.Counter()
    for instr in instructions:
        screen = instr.apply(screen)
    return screen.total()


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
