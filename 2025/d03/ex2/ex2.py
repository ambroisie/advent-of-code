#!/usr/bin/env python

import sys


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> list[list[int]]:
        return [[int(c) for c in line] for line in input]

    def max_joltage(bank: list[int]) -> int:
        joltage = 0
        for length in range(12, 0, -1):
            assert length <= len(bank)  # Sanity check
            first = bank.index(max(bank[: len(bank) - length + 1]))
            joltage = joltage * 10 + bank[first]
            bank = bank[first + 1 :]
        return joltage

    batteries = parse(input)
    return sum(map(max_joltage, batteries))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
