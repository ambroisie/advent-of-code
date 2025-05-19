#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    CPY = "cpy"
    INC = "inc"
    DEC = "dec"
    JNZ = "jnz"


class Instruction(NamedTuple):
    op: Op
    x: str
    y: str | None = None

    @classmethod
    def from_str(cls, input: str) -> "Instruction":
        op, *rest = input.split()
        return cls(Op(op), *rest)


def solve(input: str) -> int:
    def parse(input: str) -> list[Instruction]:
        return [Instruction.from_str(line) for line in input.splitlines()]

    def fibonacci(n: int) -> int:
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a + b
        return b

    instructions = parse(input)
    fib_n = int(instructions[2].x) + int(instructions[5].x)
    mult = int(instructions[16].x)
    fact = int(instructions[17].x)
    return fibonacci(fib_n) + mult * fact


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
