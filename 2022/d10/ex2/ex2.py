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


@dataclasses.dataclass
class CRT:
    width: int = dataclasses.field(default=40, init=False)
    height: int = dataclasses.field(default=6, init=False)
    pixels: list[list[bool]] = dataclasses.field(init=False)

    def __post_init__(self):
        self.pixels = [[False for _ in range(self.width)] for _ in range(self.height)]

    def do_pixel(self, cycle: int, x_reg: int) -> None:
        cycle -= 1  # Simpler modulo computation
        x, y = cycle % self.width, cycle // self.width % self.height
        self.pixels[y][x] = abs(x - x_reg) <= 1

    def draw(self) -> str:
        return "\n".join(
            "".join("#" if pixel else " " for pixel in line) for line in self.pixels
        )


def solve(input: list[str]) -> str:
    cpu = CPU()
    crt = CRT()
    for cycle in cpu.execute(input):
        crt.do_pixel(cycle, cpu.x)
    return crt.draw()


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
