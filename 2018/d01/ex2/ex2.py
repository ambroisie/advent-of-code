#!/usr/bin/env python

import itertools
import sys


def solve(input: str) -> int:
    def parse(input: list[str]) -> list[int]:
        return [int(n) for n in input]

    def find_duplicate(deltas: list[int]) -> int:
        start = 0
        seen = {start}
        for delta in itertools.cycle(deltas):
            start += delta
            if start in seen:
                return start
            seen.add(start)
        assert False  # Sanity check

    deltas = parse(input.splitlines())
    return find_duplicate(deltas)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
