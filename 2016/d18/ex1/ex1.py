#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse(input: str) -> set[int]:
        return {i for i, c in enumerate(input.strip()) if c == "^"}

    def is_trap(tile: int, traps: set[int]) -> bool:
        match ((tile - 1) in traps, tile in traps, (tile + 1) in traps):
            case (True, True, False):
                return True
            case (False, True, True):
                return True
            case (True, False, False):
                return True
            case (False, False, True):
                return True
            case _:
                return False

    def step_row(traps: set[int], row_length: int) -> set[int]:
        return {i for i in range(row_length) if is_trap(i, traps)}

    traps = parse(input)
    row_length = len(input.strip())
    safe_tiles = row_length - len(traps)
    for _ in range(40 - 1):
        traps = step_row(traps, row_length)
        safe_tiles += row_length - len(traps)
    return safe_tiles


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
