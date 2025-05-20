#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[int, int, int]:
        x, y, z = map(int, input.split("x"))
        return x, y, z

    def parse(input: str) -> list[tuple[int, int, int]]:
        return [parse_line(line) for line in input.splitlines()]

    def ribbon(x: int, y: int, z: int) -> int:
        bow = x * y * z
        return 2 * min(x + y, y + z, z + x) + bow

    presents = parse(input)
    return sum(ribbon(*present) for present in presents)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
