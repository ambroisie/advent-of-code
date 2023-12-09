#!/usr/bin/env python

import itertools
import sys


def solve(input: list[str]) -> int:
    def parse_line(line: str) -> list[int]:
        return [int(n) for n in line.split()]

    def parse(input: list[str]) -> list[list[int]]:
        return [parse_line(line) for line in input]

    def extrapolate(sequence: list[int]) -> int:
        diffs = [n - p for p, n in itertools.pairwise(sequence)]
        if all(n == 0 for n in diffs):
            return sequence[-1]
        return sequence[-1] + extrapolate(diffs)

    sequences = parse(input)

    return sum(extrapolate(seq[::-1]) for seq in sequences)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
