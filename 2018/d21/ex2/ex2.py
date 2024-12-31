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

    def hash_loop(n: int, seed: int, perturb: int) -> int:
        n |= 0x10000  #
        while n:
            seed += n & 0xFF
            seed &= 0xFFFFFF  # Keeps 24-bit
            seed *= perturb
            seed &= 0xFFFFFF  # Keeps 24-bit
            n >>= 8
        return seed

    # Relies heavily on input having a specific shape
    def hash_params(ip_reg: int, instructions: list[Instruction]) -> tuple[int, int]:
        def seed_index() -> int:
            for i, instr in enumerate(instructions):
                if instr.op == OpCode.BORI and instr.b == 65536:
                    return i + 1
            assert False  # Sanity check

        def perturb_index() -> int:
            for i, instr in enumerate(instructions):
                if instr.op == OpCode.BANI and instr.b == 16777215:
                    return i + 1
            assert False  # Sanity check

        seed_instr = instructions[seed_index()]
        perturb_instr = instructions[perturb_index()]

        assert seed_instr.op == OpCode.SETI  # Sanity check
        assert perturb_instr.op == OpCode.MULI  # Sanity check
        assert perturb_instr.a == perturb_instr.c  # Sanity check
        return seed_instr.a, perturb_instr.b

    def find_comparison(ip_reg: int, instructions: list[Instruction]) -> int:
        seed, perturb = hash_params(ip_reg, instructions)
        value = 0
        count = 0
        seen: set[int] = set()
        while True:
            count += (value << 8) + (value << 16)
            if (new_value := hash_loop(value, seed, perturb)) in seen:
                return value
            seen.add(new_value)
            value = new_value
        assert False  # Sanity check

    ip_reg, instructions = parse(input.splitlines())
    return find_comparison(ip_reg, instructions)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
