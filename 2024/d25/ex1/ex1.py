#!/usr/bin/env python

import itertools
import sys

Schematic = list[int]


def solve(input: str) -> int:
    def parse_schematic(input: list[str]) -> Schematic:
        return [row.count("#") - 1 for row in list(zip(*input))]

    def parse(input: str) -> tuple[list[Schematic], list[Schematic]]:
        locks: list[Schematic] = []
        keys: list[Schematic] = []

        for schematic in input.strip().split("\n\n"):
            if schematic.startswith("#####"):
                locks.append(parse_schematic(schematic.splitlines()))
            elif schematic.endswith("#####"):
                keys.append(parse_schematic(schematic.splitlines()[::-1]))
            else:
                assert False  # Sanity check

        return locks, keys

    def fits(lock: Schematic, key: Schematic) -> bool:
        return all(l + k < 6 for l, k in zip(lock, key))

    locks, keys = parse(input)
    return sum(fits(lock, key) for lock, key in itertools.product(locks, keys))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
