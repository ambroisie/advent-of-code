#!/usr/bin/env python

import collections
import enum
import sys
from typing import NamedTuple


class Op(enum.StrEnum):
    SND = "snd"
    SET = "set"
    ADD = "add"
    MUL = "mul"
    MOD = "mod"
    RCV = "rcv"
    JGZ = "jgz"


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
    freq: int | None = None
    while True:
        assert 0 <= ip < len(instructions)  # Sanity check
        instr = instructions[ip]
        ip += 1
        match instr.op:
            case Op.SND:
                freq = resolve(instr.x, registers)
            case Op.SET:
                registers[instr.x] = resolve(instr.y, registers)
            case Op.ADD:
                registers[instr.x] += resolve(instr.y, registers)
            case Op.MUL:
                registers[instr.x] *= resolve(instr.y, registers)
            case Op.MOD:
                registers[instr.x] %= resolve(instr.y, registers)
            case Op.RCV:
                if resolve(instr.x, registers) != 0:
                    assert freq is not None
                    return freq
            case Op.JGZ:
                if resolve(instr.x, registers) > 0:
                    ip += resolve(instr.y, registers) - 1  # Account auto-increment


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
