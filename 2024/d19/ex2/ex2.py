#!/usr/bin/env python

import functools
import sys


def solve(input: str) -> int:
    def parse(input: str) -> tuple[frozenset[str], list[str]]:
        towels, patterns = input.split("\n\n")
        return frozenset(towels.split(", ")), patterns.splitlines()

    @functools.cache
    def count_ways(pattern: str, towels: frozenset[str]) -> int:
        if pattern == "":
            return 1
        return sum(
            count_ways(pattern.removeprefix(towel), towels)
            for towel in towels
            if pattern.startswith(towel)
        )

    towels, patterns = parse(input)
    return sum(count_ways(pattern, towels) for pattern in patterns)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
