#!/usr/bin/env python

import dataclasses
import functools
import operator
import sys
from collections import Counter
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclasses.dataclass
class Robot:
    pos: Point
    vel: Point

    def step(self, dims: Point, delta: int = 1) -> "Robot":
        x, y = self.pos.x + self.vel.x * delta, self.pos.y + self.vel.y * delta
        return Robot(
            Point(x % dims.x, y % dims.y),
            self.vel,
        )


def solve(input: str) -> int:
    def parse_robot(input: str) -> Robot:
        pos, vel = map(lambda s: s.split("=")[1], input.split(" "))
        return Robot(
            Point(*map(int, pos.split(","))),
            Point(*map(int, vel.split(","))),
        )

    def parse(input: list[str]) -> list[Robot]:
        return [parse_robot(line) for line in input]

    def compute_safety(robots: list[Robot], dims: Point) -> int:
        mid_x, mid_y = dims.x // 2, dims.y // 2
        counts: Counter[tuple[bool, bool]] = Counter()
        for x, y in map(lambda robot: robot.pos, robots):
            if x == mid_x or y == mid_y:
                continue
            counts[(x < mid_x, y < mid_y)] += 1
        return functools.reduce(operator.mul, counts.values())

    robots = parse(input.splitlines())
    dims = Point(101, 103)
    robots = [robot.step(dims, 100) for robot in robots]
    return compute_safety(robots, dims)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
