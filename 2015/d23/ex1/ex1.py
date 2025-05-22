#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    HLF = "hlf"
    TPL = "tpl"
    INC = "inc"
    JMP = "jmp"
    JIE = "jie"
    JIO = "jio"


class Instruction(NamedTuple):
    op: Op
    x: str
    y: str | None = None

    @classmethod
    def from_str(cls, input: str) -> "Instruction":
        op, rest = input.split(None, 1)
        return cls(Op(op), *rest.split(", "))


def solve(input: str) -> int:
    def parse(input: str) -> list[Instruction]:
        return [Instruction.from_str(line) for line in input.splitlines()]

    instructions = parse(input)
    registers: dict[str, int] = {"a": 0, "b": 0}

    ip = 0
    while True:
        if ip < 0 or ip >= len(instructions):
            break
        instr = instructions[ip]
        ip += 1
        match instr.op:
            case Op.HLF:
                registers[instr.x] //= 2
            case Op.TPL:
                registers[instr.x] *= 3
            case Op.INC:
                registers[instr.x] += 1
            case Op.JMP:
                ip += int(instr.x) - 1  # Account auto-increment
            case Op.JIE:
                assert instr.y is not None
                if registers[instr.x] % 2 == 0:
                    ip += int(instr.y) - 1  # Account auto-increment
            case Op.JIO:
                assert instr.y is not None
                if registers[instr.x] == 1:
                    ip += int(instr.y) - 1  # Account auto-increment
    return registers["b"]


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
