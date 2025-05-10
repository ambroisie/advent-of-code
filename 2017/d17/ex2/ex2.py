#!/usr/bin/env python

import collections
import sys


def solve(input: str) -> int:
    def parse(input: str) -> int:
        return int(input.strip())

    lock = collections.deque([0])
    step = parse(input)
    for i in range(1, 50000000 + 1):
        lock.rotate(-step)
        lock.append(i)
    return lock[lock.index(0) + 1]


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
