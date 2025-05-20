#!/usr/bin/env python

import collections
import sys


def solve(input: str) -> int:
    directions = collections.Counter(input.strip())
    return directions["("] - directions[")"]


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
