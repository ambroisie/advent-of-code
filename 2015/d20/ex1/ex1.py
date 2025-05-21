#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    needed = int(input.strip())
    presents = [0] * (needed // 10)  # Surely this should be enough houses
    for i in range(1, len(presents)):
        for j in range(i, len(presents), i):
            presents[j] += 10 * i
    for i, total in enumerate(presents):
        if total >= needed:
            return i
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
