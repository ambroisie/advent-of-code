#!/usr/bin/env python

import sys
from typing import List


def run_op(op_codes: List[int]) -> None:
    for index in range(0, len(op_codes), 4):  # Move every 4 positions
        op = op_codes[index]
        if op == 99:  # Halt
            return
        if op == 1:  # Sum
            lhs, rhs, dest = op_codes[index + 1 : index + 4]
            op_codes[dest] = op_codes[lhs] + op_codes[rhs]
        if op == 2:  # Multiplication
            lhs, rhs, dest = op_codes[index + 1 : index + 4]
            op_codes[dest] = op_codes[lhs] * op_codes[rhs]


def main() -> None:
    op_codes = [int(n) for n in sys.stdin.read().split(",")]
    # Specified modifications
    op_codes[1] = 12
    op_codes[2] = 2

    run_op(op_codes)

    print(op_codes[0])


if __name__ == "__main__":
    main()
