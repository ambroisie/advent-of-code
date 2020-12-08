#!/usr/bin/env python


import sys
from copy import deepcopy
from typing import List, Tuple


def run(code: List[Tuple[str, int]]) -> Tuple[int, bool]:
    accumulator = 0
    rip = 0

    def acc(val: int) -> None:
        nonlocal accumulator
        nonlocal rip
        accumulator += val
        rip += 1

    def nop(val: int) -> None:
        nonlocal rip
        rip += 1

    def jmp(val: int) -> None:
        nonlocal rip
        rip += val

    instrs = {
        "acc": acc,
        "jmp": jmp,
        "nop": nop,
    }
    seen = set()

    while rip not in seen and rip < len(code):
        seen |= {rip}
        func = instrs[code[rip][0]]
        func(code[rip][1])

    return accumulator, rip == len(code)


def solve(raw: List[str]) -> int:
    code = [(line[:3], int(line[3:])) for line in raw]
    lut = {"jmp": "nop", "nop": "jmp"}
    for i in range(len(code)):
        if code[i][0] not in lut:
            continue
        new_code = deepcopy(code)
        new_code[i] = lut[new_code[i][0]], new_code[i][1]
        val, halted = run(new_code)
        if halted:
            return val
    assert False  # Sanity check


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
