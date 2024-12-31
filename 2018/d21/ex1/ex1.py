#!/usr/bin/env python

import copy
import enum
import sys
from typing import NamedTuple


class OpCode(enum.StrEnum):
    ADDR = "addr"
    ADDI = "addi"
    MULR = "mulr"
    MULI = "muli"
    BANR = "banr"
    BANI = "bani"
    BORR = "borr"
    BORI = "bori"
    SETR = "setr"
    SETI = "seti"
    GTIR = "gtir"
    GTRI = "gtri"
    GTRR = "gtrr"
    EQIR = "eqir"
    EQRI = "eqri"
    EQRR = "eqrr"

    def apply(self, registers: list[int], a: int, b: int, c: int) -> list[int]:
        registers = copy.deepcopy(registers)
        if self == OpCode.ADDR:
            registers[c] = registers[a] + registers[b]
        if self == OpCode.ADDI:
            registers[c] = registers[a] + b
        if self == OpCode.MULR:
            registers[c] = registers[a] * registers[b]
        if self == OpCode.MULI:
            registers[c] = registers[a] * b
        if self == OpCode.BANR:
            registers[c] = registers[a] & registers[b]
        if self == OpCode.BANI:
            registers[c] = registers[a] & b
        if self == OpCode.BORR:
            registers[c] = registers[a] | registers[b]
        if self == OpCode.BORI:
            registers[c] = registers[a] | b
        if self == OpCode.SETR:
            registers[c] = registers[a]
        if self == OpCode.SETI:
            registers[c] = a
        if self == OpCode.GTIR:
            registers[c] = a > registers[b]
        if self == OpCode.GTRI:
            registers[c] = registers[a] > b
        if self == OpCode.GTRR:
            registers[c] = registers[a] > registers[b]
        if self == OpCode.EQIR:
            registers[c] = a == registers[b]
        if self == OpCode.EQRI:
            registers[c] = registers[a] == b
        if self == OpCode.EQRR:
            registers[c] = registers[a] == registers[b]
        return registers


class Instruction(NamedTuple):
    op: OpCode
    a: int
    b: int
    c: int

    def apply(self, registers: list[int]) -> list[int]:
        return self.op.apply(registers, self.a, self.b, self.c)


def solve(input: str) -> int:
    def parse_instruction(input: str) -> Instruction:
        op, *values = input.split()
        return Instruction(OpCode(op), *map(int, values))

    def parse(input: list[str]) -> tuple[int, list[Instruction]]:
        ip = int(input[0].removeprefix("#ip "))
        return ip, [parse_instruction(line) for line in input[1:]]

    # Relies on the input having a singular `EQRR` instruction
    def find_comparison(ip_reg: int, instructions: list[Instruction]) -> int:
        registers = [0] * 6
        while (ip := registers[ip_reg]) < len(instructions):
            instr = instructions[ip]
            if instr.op == OpCode.EQRR:
                operands = {instr.a, instr.b}
                assert 0 in operands  # Sanity check
                operands.remove(0)
                return registers[operands.pop()]
            registers = instr.apply(registers)
            registers[ip_reg] += 1
        assert False  # Sanity check

    ip_reg, instructions = parse(input.splitlines())
    return find_comparison(ip_reg, instructions)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
