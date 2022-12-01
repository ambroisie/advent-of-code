#!/usr/bin/env python

import sys


def solve(input: list[list[int]]) -> int:
    totals = sorted(map(lambda l: sum(l, start=0), input), reverse=True)
    return sum(totals[:3])


def main() -> None:
    input = [
        [int(line) for line in group.splitlines()]
        for group in sys.stdin.read().split("\n\n")
        if group
    ]
    print(solve(input))


if __name__ == "__main__":
    main()
