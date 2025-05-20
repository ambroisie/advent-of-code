#!/usr/bin/env python

import enum
import math
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    CPY = "cpy"
    INC = "inc"
    DEC = "dec"
    JNZ = "jnz"
    TGL = "tgl"


class Instruction(NamedTuple):
    op: Op
    x: str
    y: str | None = None

    @classmethod
    def from_str(cls, input: str) -> "Instruction":
        op, *rest = input.split()
        return cls(Op(op), *rest)

    def toggle(self) -> "Instruction":
        if self.y is None:
            op = Op.DEC if self.op == Op.INC else Op.INC
        else:
            op = Op.CPY if self.op == Op.JNZ else Op.JNZ
        return Instruction(op, self.x, self.y)


def solve(input: str) -> int:
    def parse(input: str) -> list[Instruction]:
        return [Instruction.from_str(line) for line in input.splitlines()]

    instructions = parse(input)

    num_eggs = 12
    c = int(instructions[19].x)
    d = int(instructions[20].x)
    return math.factorial(num_eggs) + c * d


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
