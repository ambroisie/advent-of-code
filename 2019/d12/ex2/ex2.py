#!/usr/bin/env python


import re
import sys
from copy import deepcopy
from dataclasses import dataclass
from math import gcd
from typing import List


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


def lcm(a: int, b: int, c: int) -> int:
    def lcm_2(a: int, b: int) -> int:
        return abs(a * b) // gcd(a, b)

    return lcm_2(lcm_2(a, b), c)


def main() -> None:
    asteroids = [line_to_pos(line) for line in sys.stdin.readlines()]
    velocities = [Position(0, 0, 0) for __ in asteroids]

    cycles: List[int] = []
    for attr in ("x", "y", "z"):
        all_prev_pos = [deepcopy(asteroids)]
        all_prev_vel = [deepcopy(velocities)]
        i = 0

        found = False
        while not found:
            i += 1
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

            for old_pos, old_vel in zip(all_prev_pos, all_prev_vel):
                if all(
                    n.__getattribute__(attr) == o.__getattribute__(attr)
                    for n, o in zip(asteroids, old_pos)
                ) and all(
                    n.__getattribute__(attr) == o.__getattribute__(attr)
                    for n, o in zip(velocities, old_vel)
                ):
                    found = True

        cycles.append(i)

    print(lcm(*cycles))


if __name__ == "__main__":
    main()
