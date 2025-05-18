#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse_triple(input: str) -> tuple[int, int, int]:
        nums = tuple(map(int, input.split()))
        assert len(nums) == 3
        return nums

    def parse(input: str) -> list[tuple[int, int, int]]:
        return [parse_triple(line) for line in input.splitlines()]

    def is_triangle(x: int, y: int, z: int) -> bool:
        return (x + y) > z and (x + z) > y and (y + z) > x

    numbers = parse(input)
    return sum(is_triangle(*t) for t in numbers)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
