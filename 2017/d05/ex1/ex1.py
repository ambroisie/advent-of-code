#!/usr/bin/env python

import itertools
import sys


def solve(input: str) -> int:
    def parse(input: str) -> list[int]:
        return [int(n) for n in input.splitlines()]

    instructions = parse(input)
    offset = 0
    for i in itertools.count():
        if offset < 0 or offset >= len(instructions):
            return i
        instructions[offset] += 1
        offset += instructions[offset] - 1  # Account for previous increment
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
