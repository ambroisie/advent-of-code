#!/usr/bin/env python

import itertools
import sys


def solve(input: str) -> int:
    def parse(input: str) -> dict[int, int]:
        return {
            depth: range
            for depth, range in (map(int, l.split(": ")) for l in input.splitlines())
        }

    def would_catch(depth: int, range: int, offset: int) -> bool:
        cycle_length = (range - 1) * 2
        return (depth + offset) % cycle_length == 0

    def compute_delay(firewall: dict[int, int]) -> int:
        for i in itertools.count():
            if any(would_catch(depth, range, i) for depth, range in firewall.items()):
                continue
            return i
        assert False  # Sanity check

    firewall = parse(input)
    return compute_delay(firewall)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
