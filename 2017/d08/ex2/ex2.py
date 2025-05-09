#!/usr/bin/env python

import enum
import itertools
import operator
import sys
from collections import defaultdict
from typing import NamedTuple


class Operation(enum.StrEnum):
    INC = "inc"
    DEC = "dec"


class Comparator(enum.StrEnum):
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    EQ = "=="
    NE = "!="

    def __call__(self, lhs: int, rhs: int) -> bool:
        return getattr(operator, self.name.lower())(lhs, rhs)


class Condition(NamedTuple):
    target: str
    comp: Comparator
    value: int

    def eval(self, registers: dict[str, int]) -> bool:
        return self.comp(registers[self.target], self.value)


class Instruction(NamedTuple):
    target: str
    op: Operation
    amount: int
    condition: Condition


def solve(input: str) -> int:
    def parse_line(line: str) -> Instruction:
        target, op, amount, _, comp_target, comp_op, comp_value = line.split()
        return Instruction(
            target,
            Operation(op),
            int(amount),
            Condition(comp_target, Comparator(comp_op), int(comp_value)),
        )

    def parse(input: str) -> list[Instruction]:
        return [parse_line(line) for line in input.splitlines()]

    program = parse(input)
    regs: dict[str, int] = defaultdict(int)
    max_reg = 0
    for instr in program:
        if not instr.condition.eval(regs):
            continue
        regs[instr.target] += instr.amount * (1 if instr.op == Operation.INC else -1)
        max_reg = max(itertools.chain(regs.values(), [max_reg]))
    return max_reg


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
