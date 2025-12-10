#!/usr/bin/env python

import sys
from typing import NamedTuple

import z3


class Machine(NamedTuple):
    lights: tuple[bool, ...]
    buttons: list[list[int]]
    joltage: list[int]

    @classmethod
    def from_str(cls, input: str) -> "Machine":
        raw_lights, *raw_buttons, raw_joltage = input.split()
        lights = [c == "#" for c in raw_lights[1:-1]]
        buttons = [[int(n) for n in button[1:-1].split(",")] for button in raw_buttons]
        joltage = [int(n) for n in raw_joltage[1:-1].split(",")]
        return cls(tuple(lights), buttons, joltage)


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> list[Machine]:
        return [Machine.from_str(line) for line in input]

    def joltage_presses(machine: Machine) -> int:
        optimizer = z3.Optimize()

        presses = [z3.Int(f"button_{i}") for i, _ in enumerate(machine.buttons)]

        # Buttons can't be pressed negative times
        for count in presses:
            optimizer.add(count >= 0)
        # Sum of counters must match their goals
        for i, joltage_goal in enumerate(machine.joltage):
            joltage = sum(
                count
                for count, button in zip(presses, machine.buttons, strict=True)
                if i in button
            )
            optimizer.add(joltage == joltage_goal)
        # Minimize button presses
        optimizer.minimize(sum(presses))

        assert optimizer.check() == z3.sat  # Sanity check

        model = optimizer.model()
        return sum(model[b].as_long() for b in presses)  # type: ignore

    manual = parse(input)
    return sum(joltage_presses(machine) for machine in manual)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
