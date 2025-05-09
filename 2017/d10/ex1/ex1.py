#!/usr/bin/env python

import copy
import sys


def solve(input: str) -> int:
    def parse(input: str) -> list[int]:
        return [int(n) for n in input.split(",")]

    def run_round(lengths: list[int], circle: list[int]) -> list[int]:
        circle = copy.deepcopy(circle)
        cur_pos = 0
        skip_size = 0
        for n in lengths:
            # Invalid length
            if n > len(circle):
                continue
            # Reverse
            for i, j in zip(
                range(cur_pos, cur_pos + n // 2),
                # Avoid off-by-one by going further than necessary
                range(cur_pos + n - 1, cur_pos, -1),
            ):
                i %= len(circle)
                j %= len(circle)
                circle[i], circle[j] = circle[j], circle[i]
            # Move
            cur_pos += n + skip_size
            # Increase
            skip_size += 1
        return circle

    lengths = parse(input)
    circle = list(range(256))
    circle = run_round(lengths, circle)
    return circle[0] * circle[1]


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
