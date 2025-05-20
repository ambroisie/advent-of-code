#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    CPY = "cpy"
    INC = "inc"
    DEC = "dec"
    JNZ = "jnz"
    OUT = "out"


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

    def next_signal_int(n: int) -> int:
        res = 0b10
        while res < n:
            res = (res << 2) | res
        return res

    instructions = parse(input)
    bc = int(instructions[1].x) * int(instructions[2].x)
    return next_signal_int(bc) - bc


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
