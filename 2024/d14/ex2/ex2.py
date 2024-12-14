#!/usr/bin/env python

import dataclasses
import functools
import itertools
import sys
from typing import Literal, NamedTuple


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

    def find_tree(robots: list[Robot], dims: Point) -> int:
        def compute_positions(step: int) -> list[Point]:
            return [robot.step(dims, step).pos for robot in robots]

        def compute_variance(values: list[int]) -> float:
            avg = sum(values) / len(values)
            variance = sum((n - avg) ** 2 for n in values) / len(values)
            return variance

        def cluster_variance(step: int, dimension: Literal["x", "y"]) -> float:
            return compute_variance(
                [getattr(p, dimension) for p in compute_positions(step)]
            )

        # The tree should have robots clustered together in X and Y
        cluster_x = min(
            range(dims.x),
            key=functools.partial(cluster_variance, dimension="x"),
        )
        cluster_y = min(
            range(dims.y),
            key=functools.partial(cluster_variance, dimension="y"),
        )

        # And those clusers should repeat modulo each dimension
        for i in itertools.count(cluster_x, step=dims.x):
            if i % dims.y == cluster_y:
                return i
        assert False  # Sanity check

    robots = parse(input.splitlines())
    dims = Point(101, 103)
    return find_tree(robots, dims)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
