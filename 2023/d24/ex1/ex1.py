#!/usr/bin/env python

import itertools
import sys
from decimal import Decimal
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int


class HailStone(NamedTuple):
    pos: Point
    vel: Point


def solve(input: list[str]) -> int:
    def parse_line(line: str) -> HailStone:
        pos, vel = line.split(" @ ")
        return HailStone(
            Point(*map(int, pos.split(", "))), Point(*map(int, vel.split(", ")))
        )

    def parse(input: list[str]) -> list[HailStone]:
        return [parse_line(line) for line in input]

    def intersections(hailstones: list[HailStone], boundaries: tuple[int, int]) -> int:
        def intersects(a: HailStone, b: HailStone) -> bool:
            # According to wikipedia, if:
            # x = a_px + t * a_vx = b_px + u * b_vx
            # y = a_py + t * a_vy = b_py + u * b_vy
            # then:
            # t = ((a_px-b_px)*(-b_vy) - (a_py-b_py)*(-b_vx)) / ((-a_vx)*(-b_vy) - (-a_vy)*(-b_vx))
            # u = ((a_px-b_px)*(-a_vy) - (a_py-b_py)*(-a_vx)) / ((-a_vx)*(-b_vy) - (-a_vy)*(-b_vx))
            (a_px, a_py, _), (a_vx, a_vy, _) = a
            (b_px, b_py, _), (b_vx, b_vy, _) = b

            # Use rationals for extra precision, just in case
            denom = Decimal(a_vx * b_vy - a_vy * b_vx)

            # Parallel lines
            if denom == 0:
                return False

            t = ((a_px - b_px) * (-b_vy) - (a_py - b_py) * (-b_vx)) / denom
            u = ((a_px - b_px) * (-a_vy) - (a_py - b_py) * (-a_vx)) / denom

            # Intersects in the past
            if t < 0 or u < 0:
                return False

            x = a_px + t * a_vx
            y = a_py + t * a_vy

            # Outside our observation area
            if not boundaries[0] <= x <= boundaries[1]:
                return False
            if not boundaries[0] <= y <= boundaries[1]:
                return False

            return True

        return sum(intersects(a, b) for a, b in itertools.combinations(hailstones, 2))

    hailstones = parse(input)
    return intersections(hailstones, (200000000000000, 400000000000000))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
