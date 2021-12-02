#!/usr/bin/env python

import itertools
import sys
from typing import List


def solve(input: List[str]) -> int:
    x, y = 0, 0

    for instruction in input:
        dir, length_ = instruction.split(" ")
        length = int(length_)
        if dir == "forward":
            x += length
        elif dir == "down":
            y += length
        elif dir == "up":
            y -= length
        else:
            assert False

    return x * y


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
