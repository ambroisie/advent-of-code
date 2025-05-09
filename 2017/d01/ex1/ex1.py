#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    nums = [int(n) for n in input.strip()]
    return sum(n for n, m in zip(nums, nums[1:] + nums[:1]) if n == m)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
