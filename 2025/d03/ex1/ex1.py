#!/usr/bin/env python

import sys


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> list[list[int]]:
        return [[int(c) for c in line] for line in input]

    def max_joltage(bank: list[int]) -> int:
        first = bank.index(max(bank[:-1]))
        second = bank.index(max(bank[first + 1 :]))
        return bank[first] * 10 + bank[second]

    batteries = parse(input)
    return sum(map(max_joltage, batteries))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
