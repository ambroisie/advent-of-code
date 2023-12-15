#!/usr/bin/env python

import sys


def solve(input: list[str]) -> int:
    def compute_hash(string: str) -> int:
        res = 0

        for c in string:
            res += ord(c)
            res *= 17
            res %= 256

        return res

    return sum(map(compute_hash, input))


def main() -> None:
    input = sys.stdin.read().splitlines()
    assert len(input) == 1  # Sanity check
    print(solve(input[0].split(",")))


if __name__ == "__main__":
    main()
