#!/usr/bin/env python

import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Particle(NamedTuple):
    pos: Point
    vel: Point
    acc: Point

    @classmethod
    def from_str(cls, input: str) -> "Particle":
        p, v, a = input.split(", ")
        return cls(
            Point(*map(int, p[3:-1].split(","))),
            Point(*map(int, v[3:-1].split(","))),
            Point(*map(int, a[3:-1].split(","))),
        )


def solve(input: str) -> int:
    def parse(input: str) -> list[Particle]:
        return [Particle.from_str(line) for line in input.splitlines()]

    def dist(point: Point, other: Point) -> int:
        return sum(abs(a - b) for a, b in zip(point, other))

    particles = parse(input)
    orig = Point(0, 0, 0)
    # Lowest acceleration will be closest to origin as time tends to infinity
    # Same logic for velocity and position
    closest_particle = min(
        particles,
        key=lambda p: (dist(p.acc, orig), dist(p.vel, orig), dist(p.pos, orig)),
    )
    return particles.index(closest_particle)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
