#!/usr/bin/env python
import itertools
import re
import sys
from dataclasses import dataclass
from typing import Dict, Iterator, List


@dataclass
class Mask:
    ones: int
    zeros: int


Memory = Dict[int, int]


def gen_floats(xs: int) -> Iterator[int]:
    x_positions = [i for i in range(36) if (1 << i) & xs]

    return (
        sum(1 << x_positions[i] for i, v in enumerate(val) if v == 1)
        for val in itertools.product([0, 1], repeat=len(x_positions))
    )


def solve(raw: List[str]) -> int:
    mask = Mask(
        0,
        (2 << 36) - 1,
    )
    mem_pattern = re.compile("mem\\[([0-9]+)\\] = ([0-9]+)")
    mask_pattern = re.compile("mask = ([01X]+)")
    mem: Memory = {}
    for instr in raw:
        if (mem_match := mem_pattern.match(instr)) is not None:
            addr, val = int(mem_match.group(1)), int(mem_match.group(2))
            addr |= mask.ones
            xs = ~mask.ones & mask.zeros
            addr &= ~xs  # Put floating bits to 0
            for x in gen_floats(xs):
                mem[addr | x] = val
        elif (mask_match := mask_pattern.match(instr)) is not None:
            ones = int(mask_match.group(1).replace("X", "0"), 2)
            zeros = int(mask_match.group(1).replace("X", "1"), 2)
            mask = Mask(ones, zeros)
    return sum(mem.values())


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
