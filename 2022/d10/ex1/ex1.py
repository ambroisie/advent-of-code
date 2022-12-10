#!/usr/bin/env python

import dataclasses
import sys
from collections.abc import Iterable, Iterator


@dataclasses.dataclass
class CPU:
    x: int = dataclasses.field(default=1, init=False)
    cycle: int = dataclasses.field(default=0, init=False)

    def execute(self, instructions: Iterable[str]) -> Iterator[int]:
        for instr in instructions:
            yield from self.execute_once(instr)

    def execute_once(self, instruction: str) -> Iterator[int]:
        if instruction == "noop":
            yield from self.__do_cycle()
        else:
            assert instruction.startswith("addx")
            yield from self.__do_cycle(2)
            self.x += int(instruction.split()[1])

    def __do_cycle(self, cycles: int = 1) -> Iterator[int]:
        for _ in range(cycles):
            self.cycle += 1
            yield self.cycle


def solve(input: list[str]) -> int:
    cpu = CPU()
    return sum(cycle * cpu.x for cycle in cpu.execute(input) if (cycle % 40) == 20)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
