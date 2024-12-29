#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def reduce_polymer(polymer: str) -> str:
        for i in range(26):
            lower, upper = chr(ord("a") + i), chr(ord("A") + i)
            polymer = polymer.replace(lower + upper, "")
            polymer = polymer.replace(upper + lower, "")
        return polymer

    def fully_reduced(polymer: str) -> str:
        while True:
            reduced = reduce_polymer(polymer)
            if reduced == polymer:
                return polymer
            polymer = reduced
        assert False  # Sanity check

    def remove_defective(polymer: str, unit: str) -> str:
        return polymer.replace(unit.lower(), "").replace(unit.upper(), "")

    polymer = input.strip()
    return min(
        len(fully_reduced(remove_defective(polymer, chr(ord("a") + i))))
        for i in range(26)
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
