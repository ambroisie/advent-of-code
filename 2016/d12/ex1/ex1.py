#!/usr/bin/env python

import collections
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

    def resolve(y: str | None, registers: dict[str, int]) -> int:
        assert y is not None  # Sanity check
        try:
            return int(y)
        except ValueError:
            return registers[y]

    instructions = parse(input)
    registers: dict[str, int] = collections.defaultdict(int)

    ip = 0
    while True:
        if ip < 0 or ip >= len(instructions):
            break
        instr = instructions[ip]
        ip += 1
        match instr.op:
            case Op.CPY:
                assert instr.y is not None
                registers[instr.y] = resolve(instr.x, registers)
            case Op.INC:
                registers[instr.x] += 1
            case Op.DEC:
                registers[instr.x] -= 1
            case Op.JNZ:
                if resolve(instr.x, registers) != 0:
                    ip += resolve(instr.y, registers) - 1  # Account auto-increment
    return registers["a"]


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
