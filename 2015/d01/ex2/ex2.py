#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    BASEMENT = -1
    current = 0
    for i, c in enumerate(input, start=1):
        current += 1 if c == "(" else -1
        if current == BASEMENT:
            return i
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
