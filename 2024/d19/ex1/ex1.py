#!/usr/bin/env python

import functools
import sys


def solve(input: str) -> int:
    def parse(input: str) -> tuple[frozenset[str], list[str]]:
        towels, patterns = input.split("\n\n")
        return frozenset(towels.split(", ")), patterns.splitlines()

    @functools.cache
    def is_possible(pattern: str, towels: frozenset[str]) -> bool:
        if pattern == "":
            return True
        return any(
            is_possible(pattern.removeprefix(towel), towels)
            for towel in towels
            if pattern.startswith(towel)
        )

    towels, patterns = parse(input)
    return sum(is_possible(pattern, towels) for pattern in patterns)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
