#!/usr/bin/env python


import itertools
import sys
from typing import List


def find_invalid(nums: List[int]) -> int:
    for i in range(25, len(nums)):
        num = nums[i]
        found = False
        for lhs, rhs in itertools.combinations(nums[i - 25 : i], 2):
            if lhs + rhs == num:
                found = True
                break
        if not found:
            return num
    assert False  # Sanity check


def find_weakness(nums: List[int], invalid: int) -> int:
    for i in range(len(nums) - 2):
        for j in range(i + 2, len(nums)):
            if sum(nums[i:j]) == invalid:
                return min(nums[i:j]) + max(nums[i:j])
    assert False  # Sanity check((


def solve(raw: List[str]) -> int:
    nums = [int(line) for line in raw]
    invalid = find_invalid(nums)
    return find_weakness(nums, invalid)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
