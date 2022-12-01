#!/usr/bin/env python

import sys


def solve(input: list[list[int]]) -> int:
    return max(map(sum, input), default=0)


def main() -> None:
    input = [
        [int(line) for line in group.splitlines()]
        for group in sys.stdin.read().split("\n\n")
        if group
    ]
    print(solve(input))


if __name__ == "__main__":
    main()
