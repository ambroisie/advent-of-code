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
        return Point(x, y)

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
        def found_prize(row: list[tuple[int, Point]]) -> int | None:
            for tokens, p in row:
                if p == machine.prize:
                    return tokens
            return None

        row = [
            (3 * i, Point(machine.a_delta.x * i, machine.a_delta.y * i))
            for i in range(101)
        ]
        res = found_prize(row)
        for _ in range(100):
            row = [
                (tokens + 1, Point(p.x + machine.b_delta.x, p.y + machine.b_delta.y))
                for tokens, p in row
            ]
            tmp = found_prize(row)
            if tmp is None:
                continue
            if res is None:
                res = tmp
            res = min(res, tmp)
        return res

    claw_machines = parse(input)
    return sum(
        tokens for tokens in map(play_machine, claw_machines) if tokens is not None
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
