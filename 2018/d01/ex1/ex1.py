#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse(input: list[str]) -> list[int]:
        return [int(n) for n in input]

    deltas = parse(input.splitlines())
    return sum(deltas)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
