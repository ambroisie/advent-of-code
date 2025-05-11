#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    SET = "set"
    SUB = "sub"
    MUL = "mul"
    JNZ = "jnz"


class Instruction(NamedTuple):
    op: Op
    x: str
    y: str

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
    registers = {chr(ord("a") + i): 0 for i in range(8)}

    ip = 0
    total_muls = 0
    while True:
        if ip < 0 or ip >= len(instructions):
            break
        instr = instructions[ip]
        ip += 1
        match instr.op:
            case Op.SET:
                registers[instr.x] = resolve(instr.y, registers)
            case Op.SUB:
                registers[instr.x] -= resolve(instr.y, registers)
            case Op.MUL:
                registers[instr.x] *= resolve(instr.y, registers)
                total_muls += 1
            case Op.JNZ:
                if resolve(instr.x, registers) != 0:
                    ip += resolve(instr.y, registers) - 1  # Account auto-increment
    return total_muls


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
