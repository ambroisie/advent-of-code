#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def reduce_polymer(polymer: str) -> str:
        for i in range(26):
            lower, upper = chr(ord("a") + i), chr(ord("A") + i)
            polymer = polymer.replace(lower + upper, "")
            polymer = polymer.replace(upper + lower, "")
        return polymer

    polymer = input.strip()
    while True:
        reduced = reduce_polymer(polymer)
        if reduced == polymer:
            return len(polymer)
        polymer = reduced
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
