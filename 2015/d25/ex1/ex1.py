#!/usr/bin/env python

import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def parse(input: str) -> tuple[int, int]:
        *_, row, column = input.replace(".", "").split(", ")
        return int(row.split()[-1]), int(column.split()[-1])

    def mod_pow(n: int, pow: int, mod: int) -> int:
        if pow == 0:
            return 1
        if pow == 1:
            return n % mod
        res = mod_pow(n, pow // 2, mod) ** 2
        if pow % 2 == 1:
            res *= n
        return res % mod

    def lookup(row: int, column: int) -> int:
        n = column + row - 1
        top_right = n * (n + 1) // 2
        i = top_right - row
        return 20151125 * mod_pow(252533, i, 33554393) % 33554393

    row, column = parse(input)
    return lookup(row, column)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
