#!/usr/bin/env python

import itertools
import sys
from typing import NamedTuple


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

    def apply_schematic(
        lights: tuple[bool, ...],
        button: list[int],
    ) -> tuple[bool, ...]:
        assert all(n < len(lights) for n in button)  # Sanity check
        return tuple((l if i not in button else not l) for i, l in enumerate(lights))

    def start_presses(machine: Machine) -> int:
        start = tuple(False for _ in machine.lights)
        queue = [start]
        seen = {start}
        for i in itertools.count(1):
            new_queue: list[tuple[bool, ...]] = []
            for p in queue:
                for button in machine.buttons:
                    n = apply_schematic(p, button)
                    # If we've seen `n` before, it was in less or equal number of steps
                    if n in seen:
                        continue
                    # If we're at the end state, we've found the fastest path
                    if n == machine.lights:
                        return i
                    # Else, explore from that state
                    new_queue.append(n)
                    seen.add(n)
            assert new_queue  # Sanity check
            queue = new_queue
        assert False  # Sanity check

    manual = parse(input)
    return sum(start_presses(machine) for machine in manual)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
