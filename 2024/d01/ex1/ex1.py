#!/usr/bin/env python

import sys


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> tuple[list[int], list[int]]:
        left, right = [], []
        for line in input:
            lhs, rhs = line.split()
            left.append(int(lhs))
            right.append(int(rhs))
        return left, right

    left, right = parse(input)
    return sum(abs(lhs - rhs) for lhs, rhs in zip(sorted(left), sorted(right)))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
