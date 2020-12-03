#!/usr/bin/env python

import sys
from math import prod
from typing import List, Tuple


def solve(trees: List[str], delta: Tuple[int, int]) -> int:
    x, y = 0, 0
    sum = 0
    while True:
        x += delta[0]
        y += delta[1]
        if y >= len(trees):
            break
        sum += trees[y][x % len(trees[0])] == "#"
    return sum


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    deltas = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    print(prod(solve(input, delt) for delt in deltas))


if __name__ == "__main__":
    main()
