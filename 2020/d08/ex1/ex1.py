#!/usr/bin/env python


import sys
from typing import List, Tuple


def run(code: List[Tuple[str, int]]) -> int:
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

    while rip not in seen:
        seen |= {rip}
        func = instrs[code[rip][0]]
        func(code[rip][1])

    return accumulator


def solve(raw: List[str]) -> int:
    return run([(line[:3], int(line[3:])) for line in raw])


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
