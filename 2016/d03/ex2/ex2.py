#!/usr/bin/env python

import itertools
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

    def transpose_triples(
        numbers: list[tuple[int, int, int]],
    ) -> list[tuple[int, int, int]]:
        res: list[tuple[int, int, int]] = []
        for l1, l2, l3 in itertools.batched(numbers, 3):
            for i in range(3):
                res.append((l1[i], l2[i], l3[i]))
        return res

    numbers = parse(input)
    numbers = transpose_triples(numbers)
    return sum(is_triangle(*t) for t in numbers)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
