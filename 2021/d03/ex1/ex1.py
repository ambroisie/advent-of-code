#!/usr/bin/env python

import itertools
import sys
from typing import List


def solve(input: List[int]) -> int:
    gamma, epsilon = 0, 0
    bit = 1

    while any(map(bool, input)):
        num_bits = sum(n % 2 for n in input)
        if num_bits >= len(input) / 2:
            gamma += bit
        else:
            epsilon += bit
        input = [n // 2 for n in input]
        bit *= 2

    return gamma * epsilon


def main() -> None:
    input = [int(line, 2) for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
