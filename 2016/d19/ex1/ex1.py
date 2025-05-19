#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def msb(n: int) -> int:
        assert n  # Sanity check
        return n.bit_length() - 1

    # https://en.wikipedia.org/wiki/Josephus_problem
    def josephus(n: int) -> int:
        return 2 * (n - (1 << msb(n))) + 1

    num_elves = int(input.strip())
    return josephus(num_elves)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
