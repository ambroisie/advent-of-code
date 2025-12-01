#!/usr/bin/env python

import itertools
import sys


def solve(input: list[str]) -> int:
    def parse_turn(input: str) -> int:
        direction = input[0]
        clicks = int(input[1:])
        return clicks * (1 if direction == "R" else -1)

    def parse(input: list[str]) -> list[int]:
        return [parse_turn(turn) for turn in input]

    turns = parse(input)
    positions = itertools.accumulate(turns, initial=50)
    return sum(pos % 100 == 0 for pos in positions)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
