#!/usr/bin/env python

import itertools
import sys

TOTAL_EGGNOG = 150


def solve(input: str) -> int:
    def parse(input: str) -> list[int]:
        return [int(line) for line in input.splitlines()]

    containers = parse(input)
    min_containers = min(
        i
        for i in range(1, len(containers) + 1)
        if any(
            sum(combination) == TOTAL_EGGNOG
            for combination in itertools.combinations(containers, i)
        )
    )
    return sum(
        sum(combination) == TOTAL_EGGNOG
        for combination in itertools.combinations(containers, min_containers)
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
