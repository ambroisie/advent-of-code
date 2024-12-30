#!/usr/bin/env python

import functools
import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> str:
    def cell_power(cell: Point, serial: int) -> int:
        rack_id = cell.x + 10
        power = rack_id * cell.y
        power += serial
        power *= rack_id
        return ((power // 100) % 10) - 5

    def total_power(top_left: Point, serial: int) -> int:
        return sum(
            cell_power(Point(top_left.x + dx, top_left.y + dy), serial)
            for dx, dy in itertools.product(range(3), repeat=2)
        )

    serial = int(input)
    cell = max(
        map(Point._make, itertools.product(range(1, 300 - 3 + 1), repeat=2)),
        key=functools.partial(total_power, serial=serial),
    )
    return f"{cell.x},{cell.y}"


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
