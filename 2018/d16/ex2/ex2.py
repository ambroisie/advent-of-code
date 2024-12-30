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


Instruction = list[int]


class Example(NamedTuple):
    before: list[int]
    data: Instruction
    after: list[int]


def solve(input: str) -> int:
    def parse_example(input: list[str]) -> Example:
        before = input[0].removeprefix("Before: [").removesuffix("]")
        data = input[1]
        after = input[2].removeprefix("After:  [").removesuffix("]")
        return Example(
            [int(n) for n in before.split(", ")],
            [int(n) for n in data.split()],
            [int(n) for n in after.split(", ")],
        )

    def parse_examples(input: str) -> list[Example]:
        return [parse_example(example.splitlines()) for example in input.split("\n\n")]

    def parse_data(input: list[str]) -> list[Instruction]:
        return [[int(n) for n in line.split()] for line in input]

    def parse(input: str) -> tuple[list[Example], list[Instruction]]:
        examples, data = input.split("\n\n\n\n")
        return parse_examples(examples), parse_data(data.splitlines())

    def find_opcodes(examples: list[Example]) -> dict[int, OpCode]:
        candidates: dict[int, set[OpCode]] = {n: set(OpCode) for n in range(16)}

        for example in examples:
            opcode, a, b, c = example.data
            candidates[opcode] &= {
                op
                for op in candidates[opcode]
                if op.apply(example.before, a, b, c) == example.after
            }

        while not all(len(ops) == 1 for ops in candidates.values()):
            singles = {
                n: next(iter(ops)) for n, ops in candidates.items() if len(ops) == 1
            }
            for n in candidates:
                if n in singles:
                    continue
                candidates[n] -= set(singles.values())
        return {n: ops.pop() for n, ops in candidates.items()}

    def run_program(data: list[Instruction], opcodes: dict[int, OpCode]) -> list[int]:
        registers = [0] * 4
        for opcode, a, b, c in data:
            registers = opcodes[opcode].apply(registers, a, b, c)
        return registers

    examples, data = parse(input)
    opcodes = find_opcodes(examples)
    registers = run_program(data, opcodes)
    return registers[0]


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
