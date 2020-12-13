#!/usr/bin/env python

import math
import sys
from typing import Dict, List


def run_contest(timings: List[int]) -> int:
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

    def chinese_remainder(residue_mapping: Dict[int, int]) -> int:
        res = 0
        prod = math.prod(residue_mapping)
        for n_i, a_i in residue_mapping.items():
            p = prod // n_i
            res += a_i * mul_inv(p, n_i) * p
        return res % prod

    residues = {t: -i for (i, t) in enumerate(timings) if t > 0}
    return chinese_remainder(residues)


def solve(raw: List[str]) -> int:
    return run_contest([int(i) if i != "x" else -1 for i in raw[1].split(",")])


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
