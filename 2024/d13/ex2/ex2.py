#!/usr/bin/env python

import dataclasses
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclasses.dataclass
class ClawMachine:
    a_delta: Point
    b_delta: Point
    prize: Point


def solve(input: str) -> int:
    def parse_button(input: str) -> Point:
        deltas = input.split(": ")[1].strip()
        x, y = map(lambda delta: int(delta.split("+")[1]), deltas.split(", "))
        return Point(x, y)

    def parse_prize(input: str) -> Point:
        coords = input.split(": ")[1].strip()
        x, y = map(lambda delta: int(delta.split("=")[1]), coords.split(", "))
        return Point(10000000000000 + x, 10000000000000 + y)

    def parse_claw_machine(input: list[str]) -> ClawMachine:
        assert len(input) == 3  # Sanity check
        return ClawMachine(
            parse_button(input[0]),
            parse_button(input[1]),
            parse_prize(input[2]),
        )

    def parse(input: str) -> list[ClawMachine]:
        return [parse_claw_machine(group.splitlines()) for group in input.split("\n\n")]

    def play_machine(machine: ClawMachine) -> int | None:
        a_dx, a_dy = machine.a_delta
        b_dx, b_dy = machine.b_delta
        px, py = machine.prize

        a = (px * b_dy - py * b_dx) // (b_dy * a_dx - b_dx * a_dy)
        b = (px * a_dy - py * a_dx) // (a_dy * b_dx - a_dx * b_dy)

        if a * a_dx + b * b_dx != px:
            return None
        if a * a_dy + b * b_dy != py:
            return None

        return 3 * a + b

    claw_machines = parse(input)
    return sum(
        tokens for tokens in map(play_machine, claw_machines) if tokens is not None
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
