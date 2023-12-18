#!/usr/bin/env python

import itertools
import sys
from enum import StrEnum
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"

    def apply(self, pos: Point, n: int = 1) -> Point:
        DIRECTIONS = {
            "U": Point(-1, 0),
            "D": Point(1, 0),
            "L": Point(0, -1),
            "R": Point(0, 1),
        }
        dx, dy = DIRECTIONS[self.value]
        return Point(pos.x + dx * n, pos.y + dy * n)


DigPlanStep = tuple[Direction, int]
DigPlan = list[DigPlanStep]


def solve(input: list[str]) -> int:
    def parse_line(line: str) -> DigPlanStep:
        _, _, color = line.split()
        color = color[2:-1]
        n = color[:-1]
        dir = {
            "0": "R",
            "1": "D",
            "2": "L",
            "3": "U",
        }[color[-1]]
        return Direction(dir), int(n, base=16)

    def parse(input: list[str]) -> DigPlan:
        return list(map(parse_line, input))

    def dig_trench(plan: DigPlan) -> list[Point]:
        points = [Point(0, 0)]

        for direction, n in plan:
            points.append(direction.apply(points[-1], n))
        # The trench should loop back to the start, make sure we don't count it twice
        if points[-1] == Point(0, 0):
            del points[-1]

        return points

    def lagoon_volume(trench: list[Point]) -> int:
        def shoelace_area(points: list[Point]) -> int:
            # Must be integer because pipes follow the grid, and can't cut squares in half
            return abs(
                sum(
                    (points[i - 1].x * points[i].y) - (points[i].x * points[i - 1].y)
                    for i in range(len(points))
                )
                // 2
            )

        def perimeter(points: list[Point]) -> int:
            res = 0

            for p, n in itertools.pairwise(itertools.chain(points, [points[0]])):
                res += abs(n.x - p.x) + abs(n.y - p.y)

            return res

        area = shoelace_area(trench)
        trench_points = perimeter(trench)
        interior_points = area - trench_points // 2 + 1
        return interior_points + trench_points

    plan = parse(input)
    trench = dig_trench(plan)
    return lagoon_volume(list(trench))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
