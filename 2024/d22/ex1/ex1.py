#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def monkey_hash(seed: int) -> int:
        MASK = (1 << 24) - 1
        seed ^= seed << 6
        seed &= MASK

        seed ^= seed >> 5
        seed &= MASK

        seed ^= seed << 11
        seed &= MASK

        return seed

    def run_rounds(seed: int) -> int:
        for _ in range(2000):
            seed = monkey_hash(seed)
        return seed

    seeds = [int(n) for n in input.splitlines()]
    return sum(map(run_rounds, seeds))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
