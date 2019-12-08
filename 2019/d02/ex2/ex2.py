#!/usr/bin/env python

import sys
from copy import deepcopy
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

    for noun in range(100):
        for verb in range(100):
            mem = deepcopy(op_codes)
            mem[1] = noun
            mem[2] = verb
            run_op(mem)
            if mem[0] == 19690720:
                print(noun * 100 + verb)
                return


if __name__ == "__main__":
    main()
