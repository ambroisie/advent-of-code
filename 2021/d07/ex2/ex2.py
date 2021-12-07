#!/usr/bin/env python

import itertools
import sys
from math import ceil, floor
from typing import List


def solve(input: List[str]) -> int:
    def fuel(dist: int) -> int:
        return dist * (dist + 1) // 2

    nums = list(int(n) for n in input[0].split(","))
    mean = sum(nums) / len(nums)

    upper = sum(fuel(abs(n - ceil(mean))) for n in nums)
    lower = sum(fuel(abs(n - floor(mean))) for n in nums)

    return min(upper, lower)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
