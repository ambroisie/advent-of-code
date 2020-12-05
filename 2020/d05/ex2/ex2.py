#!/usr/bin/env python

import sys
from typing import List


def seat_id(boarding_pass: str) -> int:
    min_x = 0
    max_x = 128
    min_y = 0
    max_y = 8

    for char in boarding_pass:
        if char == "F":
            max_x = (min_x + max_x) // 2
        elif char == "B":
            min_x = (min_x + max_x) // 2
        elif char == "L":
            max_y = (min_y + max_y) // 2
        elif char == "R":
            min_y = (min_y + max_y) // 2
    return min_x * 8 + min_y


def solve(passes: List[str]) -> int:
    ids = sorted(seat_id(p) for p in passes)

    for prev, cur in zip(ids, ids[1:]):
        if prev + 1 != cur:
            return prev + 1

    assert False  # Sanity check


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
