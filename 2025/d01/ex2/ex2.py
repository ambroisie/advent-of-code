#!/usr/bin/env python

import itertools
import sys


def sign(n: int) -> int:
    if n == 0:
        return 0
    return n // abs(n)


def solve(input: list[str]) -> int:
    def parse_turn(input: str) -> int:
        direction = input[0]
        clicks = int(input[1:])
        return clicks * (1 if direction == "R" else -1)

    def parse(input: list[str]) -> list[int]:
        return [parse_turn(turn) for turn in input]

    def count_zeros(before: int, after: int) -> int:
        delta = after - before
        to_zero = (before % 100) * -sign(delta)
        if to_zero <= 0:
            to_zero += 100
        return (abs(delta) + 100 - to_zero) // 100

    turns = parse(input)
    positions = itertools.accumulate(turns, initial=50)
    return sum(count_zeros(a, b) for a, b in itertools.pairwise(positions))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
