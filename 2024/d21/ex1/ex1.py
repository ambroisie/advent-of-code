#!/usr/bin/env python

import enum
import functools
import itertools
import sys
from typing import Literal, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


Instruction = Direction | Literal["A"]

PAD = {
    "7": Point(-3, -2),
    "8": Point(-3, -1),
    "9": Point(-3, 0),
    "4": Point(-2, -2),
    "5": Point(-2, -1),
    "6": Point(-2, 0),
    "1": Point(-1, -2),
    "2": Point(-1, -1),
    "3": Point(-1, 0),
    "0": Point(0, -1),
    "A": Point(0, 0),
}

ARROWS = {
    "^": Point(0, -1),
    "A": Point(0, 0),
    "<": Point(1, -2),
    "v": Point(1, -1),
    ">": Point(1, 0),
}

# Needs to be hash-able
InstructionList = tuple[Instruction, ...]


def solve(input: str) -> int:
    def button_paths(
        start_button: str,
        end_button: str,
        buttons: dict[str, Point],
    ) -> set[InstructionList]:
        start, end = buttons[start_button], buttons[end_button]
        sequences: set[InstructionList] = set()

        dx, dy = (end.x - start.x), (end.y - start.y)

        a_button: list[Instruction] = ["A"]  # Work around MyPy limitation
        move_x = [Direction.UP if dx < 0 else Direction.DOWN] * abs(dx)
        move_y = [Direction.LEFT if dy < 0 else Direction.RIGHT] * abs(dy)

        # Avoid moving over the gap
        if Point(end.x, start.y) in buttons.values():
            sequences.add(tuple(a_button + move_x + move_y + a_button))
        if Point(start.x, end.y) in buttons.values():
            sequences.add(tuple(a_button + move_y + move_x + a_button))

        return sequences

    @functools.cache
    def path_cost(path: InstructionList, depth: int) -> int:
        # Have we reached the actual keypad robot
        if depth == 0:
            # We start on 'A' so don't count it
            return len(path) - 1
        # Otherwise, intermediate robot must use arrow pad
        cost = sum(
            min(path_cost(path, depth - 1) for path in button_paths(start, end, ARROWS))
            for start, end in itertools.pairwise(path)
        )
        return cost

    def code_cost(code: str, depth: int) -> int:
        # We start on 'A'
        code = "A" + code
        cost = sum(
            min(path_cost(path, depth) for path in button_paths(start, end, PAD))
            for start, end in itertools.pairwise(code)
        )
        return cost

    def complexity(code: str, seq_len: int) -> int:
        return int(code.replace("A", "")) * seq_len

    codes = input.splitlines()
    return sum(complexity(code, code_cost(code, 2)) for code in codes)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
