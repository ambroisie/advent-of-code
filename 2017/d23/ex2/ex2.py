#!/usr/bin/env python

import enum
import math
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

    def is_prime(n: int) -> bool:
        if n % 2 == 0:
            return False
        for i in range(3, math.isqrt(n), 2):
            if n % i == 0:
                return False
        return True

    instructions = parse(input)
    start = int(instructions[0].y) * 100 + 100000
    end = start + 17000

    total = 0
    for n in range(start, end + 1, 17):
        total += not is_prime(n)
    return total


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
