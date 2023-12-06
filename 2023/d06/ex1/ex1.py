#!/usr/bin/env python

import math
import sys


def solve(input: list[str]) -> int:
    def parse_line(line: str) -> list[int]:
        return [int(n) for n in line.split(":")[1].split()]

    def solve(time: int, distance: int) -> int:
        # With n being the button-held-down time.
        # We want to solve: (time - n) * n > distance
        # So we want the number of intergers in ]n_1, n_2[, n_1 and n_2 roots of the quadratic
        # a = -1, b = time, c = -distance
        determinant = time**2 - 4 * distance
        if determinant <= 0:
            return 0
        max = time / 2
        delta = math.sqrt(determinant) / 2
        n_1 = max - delta
        n_2 = max + delta
        return math.ceil(n_2 - 1) - math.floor(n_1 + 1) + 1

    times, distances = map(parse_line, input)

    return math.prod(solve(t, d) for t, d in zip(times, distances))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
