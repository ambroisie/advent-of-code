#!/usr/bin/env python

import math
import sys
from typing import NamedTuple


class Disc(NamedTuple):
    num: int
    positions: int
    start_offset: int

    @classmethod
    def from_str(cls, input: str) -> "Disc":
        input = input.removeprefix("Disc #").removesuffix(".")
        split_input = input.split()
        return Disc(
            int(split_input[0]),
            int(split_input[2]),
            int(split_input[-1]),
        )


def solve(input: str) -> int:
    def parse(input: str) -> list[Disc]:
        return [Disc.from_str(line) for line in input.splitlines()]

    # https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
    def mul_inv(a: int, b: int) -> int:
        b0 = b
        x0, x1 = 0, 1
        if b == 1:
            return 1
        while a > 1:
            q = a // b
            a, b = b, a % b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += b0
        return x1

    def chinese_remainder(residue_mapping: dict[int, int]) -> int:
        res = 0
        prod = math.prod(residue_mapping)
        for n_i, a_i in residue_mapping.items():
            p = prod // n_i
            res += a_i * mul_inv(p, n_i) * p
        return res % prod

    discs = parse(input)
    residues = {disc.positions: -(disc.start_offset + disc.num) for disc in discs}
    return chinese_remainder(residues)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
