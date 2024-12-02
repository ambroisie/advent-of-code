#!/usr/bin/env python

import sys
import itertools

Report = list[int]


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> list[Report]:
        return [[int(n) for n in line.split()] for line in input]

    def is_safe(report: Report) -> bool:
        def is_increasing_safe(report: Report):
            for a, b in itertools.pairwise(report):
                if not 1 <= (b - a) <= 3:
                    return False
            return True

        return is_increasing_safe(report) or is_increasing_safe(report[::-1])

    return sum(is_safe(report) for report in parse(input))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
