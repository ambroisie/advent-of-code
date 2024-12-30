#!/usr/bin/env python

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

    def summed_area(power_map: dict[Point, int]) -> dict[Point, int]:
        res: dict[Point, int] = {}
        for p in map(Point._make, itertools.product(range(1, 300 + 1), repeat=2)):
            res[p] = (
                power_map[p]
                + res.get(Point(p.x - 1, p.y), 0)
                + res.get(Point(p.x, p.y - 1), 0)
                - res.get(Point(p.x - 1, p.y - 1), 0)
            )
        assert len(res) == len(power_map)  # Sanity check
        return res

    def sum_square(top_left: Point, size: int, summed_table: dict[Point, int]) -> int:
        bot_right = Point(top_left.x + size - 1, top_left.y + size - 1)
        return (
            summed_table[bot_right]
            - summed_table.get(Point(top_left.x - 1, bot_right.y), 0)
            - summed_table.get(Point(bot_right.x, top_left.y - 1), 0)
            + summed_table.get(Point(top_left.x - 1, top_left.y - 1), 0)
        )

    def best_square(summed_table: dict[Point, int]) -> tuple[Point, int]:
        return max(
            (
                (top_left, size)
                for size in range(1, 300 + 1)
                for top_left in map(
                    Point._make, itertools.product(range(1, 300 + 1 - size), repeat=2)
                )
            ),
            key=lambda t: sum_square(t[0], t[1], summed_table),
        )

    serial = int(input)
    power_map = {
        p: cell_power(p, serial)
        for p in map(Point._make, itertools.product(range(1, 300 + 1), repeat=2))
    }
    summed_table = summed_area(power_map)
    top_left, size = best_square(summed_table)
    return f"{top_left.x},{top_left.y},{size}"


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
