#!/usr/bin/env python

import sys
from typing import List


def solve(input: List[int]) -> int:
    return sum(prev < cur for (prev, cur) in zip(input, input[1:]))


def main() -> None:
    input = [int(line) for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
