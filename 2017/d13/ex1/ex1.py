#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse(input: str) -> dict[int, int]:
        return {
            depth: range
            for depth, range in (map(int, l.split(": ")) for l in input.splitlines())
        }

    def would_catch(depth: int, range: int) -> bool:
        cycle_length = (range - 1) * 2
        return depth % cycle_length == 0

    def compute_severity(firewall: dict[int, int]) -> int:
        return sum(
            depth * range
            for depth, range in firewall.items()
            if would_catch(depth, range)
        )

    firewall = parse(input)
    return compute_severity(firewall)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
