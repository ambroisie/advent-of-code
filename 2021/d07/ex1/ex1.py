#!/usr/bin/env python

import itertools
import sys
from typing import List


def solve(input: List[str]) -> int:
    nums = sorted(int(n) for n in input[0].split(","))
    median = nums[len(nums) // 2]

    return sum(abs(n - median) for n in nums)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
