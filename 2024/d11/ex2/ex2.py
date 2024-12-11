#!/usr/bin/env python

import sys
from collections import Counter


def solve(input: str) -> int:
    def parse(input: str) -> Counter[int]:
        return Counter(int(n) for n in input.split())

    def blink(stones: Counter[int]) -> Counter[int]:
        res: Counter[int] = Counter()
        for n, count in stones.items():
            if n == 0:
                res[1] += count
            elif len(str(n)) % 2 == 0:
                s = str(n)
                lhs, rhs = s[: len(s) // 2], s[len(s) // 2 :]
                res[int(lhs)] += count
                res[int(rhs)] += count
            else:
                res[n * 2024] += count
        return res

    stones = parse(input)
    for _ in range(75):
        stones = blink(stones)
    return sum(stones.values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
