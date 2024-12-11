#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse(input: str) -> list[int]:
        return [int(n) for n in input.split()]

    def blink(stones: list[int]) -> list[int]:
        res: list[int] = []
        for n in stones:
            if n == 0:
                res.append(1)
            elif len(str(n)) % 2 == 0:
                s = str(n)
                lhs, rhs = s[: len(s) // 2], s[len(s) // 2 :]
                res.extend((int(lhs), int(rhs)))
            else:
                res.append(n * 2024)
        return res

    stones = parse(input)
    for _ in range(25):
        stones = blink(stones)
    return len(stones)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
