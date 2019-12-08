#!/usr/bin/env python
import sys
from typing import List


def solve(nums: List[int]) -> int:
    return sum(num // 3 - 2 for num in nums)


def main() -> None:
    print(solve(list(int(lines) for lines in sys.stdin)))


if __name__ == "__main__":
    main()
