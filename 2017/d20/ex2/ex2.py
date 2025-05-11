#!/usr/bin/env python

import collections
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

    def tick(self) -> "Particle":
        pos, vel, acc = self
        vel = Point(*((v + a) for v, a in zip(vel, acc)))
        pos = Point(*((p + v) for p, v in zip(pos, vel)))
        return Particle(pos, vel, acc)


def solve(input: str) -> int:
    def parse(input: str) -> list[Particle]:
        return [Particle.from_str(line) for line in input.splitlines()]

    def tick(particles: list[Particle]) -> list[Particle]:
        particles = [p.tick() for p in particles]
        positions = collections.Counter(p.pos for p in particles)
        return [p for p in particles if positions[p.pos] == 1]

    particles = parse(input)
    # Guesstimate that 1000 iterations is enough to process all colisions
    for _ in range(1000):
        particles = tick(particles)
    return len(particles)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
