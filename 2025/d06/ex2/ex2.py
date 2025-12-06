#!/usr/bin/env python

import enum
import functools
import operator
import sys


class Op(enum.StrEnum):
    ADD = "+"
    MUL = "*"


def solve(input: list[str]) -> int:
    def from_cephalopod(input: list[str]) -> list[str]:
        transposed = list(map("".join, zip(*input, strict=True)))
        # If a value is only spaces, it should become newlines in the transpose
        transposed = [n if not n.isspace() else "\n" for n in transposed]
        return " ".join(transposed).splitlines()

    def parse(input: list[str]) -> tuple[list[list[int]], list[Op]]:
        raw_nums, raw_ops = input[:-1], input[-1]
        matrix = [[int(n) for n in line.split()] for line in from_cephalopod(raw_nums)]
        ops = [Op(c) for c in raw_ops.split()]
        return matrix, ops

    def apply(op: Op, nums: list[int]) -> int:
        f = {
            Op.ADD: operator.add,
            Op.MUL: operator.mul,
        }[op]
        return functools.reduce(f, nums)

    matrix, ops = parse(input)
    return sum(apply(op, nums) for op, nums in zip(ops, matrix, strict=True))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
