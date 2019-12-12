#!/usr/bin/env python


import re
import sys
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int
    z: int


def line_to_pos(l: str) -> Position:
    "<x=4, y=1, z=1>"
    regex = r"<x=(?P<x>[^,]*), y=(?P<y>[^,]*), z=(?P<z>[^,]*)>"
    match = re.search(regex, l)
    assert match is not None  # Sanity check
    return Position(*(int(match.group(g)) for g in ("x", "y", "z")))


def main() -> None:
    asteroids = [line_to_pos(line) for line in sys.stdin.readlines()]
    velocities = [Position(0, 0, 0) for __ in asteroids]

    for __ in range(1000):
        for orig, v in zip(asteroids, velocities):
            for other in asteroids:
                if orig.x != other.x:
                    v.x += 1 if orig.x < other.x else -1
                if orig.y != other.y:
                    v.y += 1 if orig.y < other.y else -1
                if orig.z != other.z:
                    v.z += 1 if orig.z < other.z else -1

        for asteroid, v in zip(asteroids, velocities):
            asteroid.x += v.x
            asteroid.y += v.y
            asteroid.z += v.z

    pot = (abs(p.x) + abs(p.y) + abs(p.z) for p in asteroids)
    kin = (abs(v.x) + abs(v.y) + abs(v.z) for v in velocities)

    print(sum(p * k for p, k in zip(pot, kin)))


if __name__ == "__main__":
    main()
