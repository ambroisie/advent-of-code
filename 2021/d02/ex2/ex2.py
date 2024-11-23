#!/usr/bin/env python

import sys
from typing import List


def solve(input: List[str]) -> int:
    x, y, aim = 0, 0, 0

    for instruction in input:
        dir, length_ = instruction.split(" ")
        length = int(length_)
        if dir == "forward":
            x += length
            y += length * aim
        elif dir == "down":
            aim += length
        elif dir == "up":
            aim -= length
        else:
            assert False

    return x * y


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
