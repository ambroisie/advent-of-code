#!/usr/bin/env python

import itertools
import math
import sys
from typing import Iterator, List, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Probe(NamedTuple):
    position: Point
    velocity: Point


class Area(NamedTuple):
    min: Point
    max: Point


def solve(input: List[str]) -> int:
    def parse(line: str) -> Area:
        x_range = line.split("x=")[1].split(",")[0]
        y_range = line.split("y=")[1]

        min_x, max_x = map(int, x_range.split(".."))
        min_y, max_y = map(int, y_range.split(".."))

        # Sanity check
        assert min_x <= max_x
        assert min_y <= max_y

        return Area(Point(min_x, min_y), Point(max_x, max_y))

    def trajectory(p: Probe) -> Iterator[Probe]:
        def step(p: Probe) -> Probe:
            def drag(x: int) -> int:
                if x < 0:
                    return x + 1
                if x > 0:
                    return x - 1
                return 0

            def gravity(y: int) -> int:
                return y - 1

            pos, vel = p

            new_pos = Point(pos.x + vel.x, pos.y + vel.y)
            new_vel = Point(drag(vel.x), gravity(vel.y))

            return Probe(new_pos, new_vel)

        while True:
            yield (p := step(p))

    def hits_target(probe: Probe, area: Area) -> bool:
        # Too lazy to find an actual good condition on this loop, early break is enough
        for p in trajectory(probe):
            x, y = p.position
            # Early exit when we cannot possibly get to the area
            if y < area.min.y and p.velocity.y <= 0:
                break
            if x < area.min.x and p.velocity.x <= 0:
                break
            if x > area.max.x and p.velocity.x >= 0:
                break
            # Keep going if we're not in bounds
            if x < area.min.x or x > area.max.x:
                continue
            if y < area.min.y or y > area.max.y:
                continue
            # We are in the area
            return True
        return False

    def find_velocities(area: Area) -> Iterator[Point]:
        position = Point(0, 0)
        assert area.min.y < 0  # Sanity check, due to lower bound in loop

        # Can't overshoot after a single step
        for vx in range(0, area.max.x + 1):
            # Can't overshoot after a single step, symmetric velocity when coming down
            for vy in range(area.min.y, abs(area.min.y) + 1):
                velocity = Point(vx, vy)
                if hits_target(Probe(position, velocity), area):
                    yield velocity

    def highest_point(velocity: Point) -> Point:
        # When the y velocity is negative, the height can only go down
        of_interest = itertools.takewhile(
            lambda p: p.velocity.y >= 0, trajectory(Probe(Point(0, 0), velocity))
        )
        points = [p.position for p in of_interest]
        return max(points, key=lambda p: p.y, default=Point(0, 0))

    target_area = parse(input[0])
    velocities = set(find_velocities(target_area))
    return max(highest_point(v).y for v in velocities)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
