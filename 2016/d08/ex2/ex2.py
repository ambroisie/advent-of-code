#!/usr/bin/env python

import enum
import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Op(enum.StrEnum):
    RECT = "rect"
    ROTATE_ROW = "row"
    ROTATE_COLUMN = "column"


MAX_X, MAX_Y = 50, 6


def solve(input: str) -> str:
    def parse_line(input: str) -> tuple[Op, int, int]:
        split_input = input.split()
        if split_input[0] == "rect":
            x, y = split_input[1].split("x")
            return Op.RECT, int(x), int(y)
        op = Op(split_input[1])
        line_col, _, shift = split_input[-3:]
        return op, int(line_col[2:]), int(shift)

    def parse(input: str) -> list[tuple[Op, int, int]]:
        return [parse_line(line) for line in input.splitlines()]

    def display_message(instructions: list[tuple[Op, int, int]]) -> set[Point]:
        screen: set[Point] = set()
        for op, a, b in instructions:
            match op:
                case Op.RECT:
                    for x, y in itertools.product(range(a), range(b)):
                        screen.add(Point(x, y))
                case Op.ROTATE_ROW:
                    pixels = {p for p in screen if p.y == a}
                    screen -= pixels
                    screen.update(Point((x + b) % MAX_X, y) for x, y in pixels)
                case Op.ROTATE_COLUMN:
                    pixels = {p for p in screen if p.x == a}
                    screen -= pixels
                    screen.update(Point(x, (y + b) % MAX_Y) for x, y in pixels)
        return screen

    def display(pixels: set[Point]) -> str:
        return "\n".join(
            "".join("#" if Point(x, y) in pixels else " " for x in range(MAX_X))
            for y in range(MAX_Y)
        )

    instructions = parse(input)
    pixels = display_message(instructions)
    return display(pixels)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
