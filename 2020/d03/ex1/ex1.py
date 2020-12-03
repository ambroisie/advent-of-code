#!/usr/bin/env python

import sys
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
    print(solve(input, (3, 1)))


if __name__ == "__main__":
    main()
