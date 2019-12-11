#!/usr/bin/env python

import sys
from cmath import phase
from itertools import groupby
from math import gcd, pi
from pprint import pprint
from typing import NamedTuple, Set, Tuple


class Position(NamedTuple):
    x: int
    y: int


def pos_to_angle_dist(pos: Position) -> Tuple[float, float]:
    cartesian = complex(*pos)
    angle = phase(cartesian)
    if angle < -pi / 2:
        angle += 2.5 * pi
    else:
        angle += pi / 2
    return (angle, abs(cartesian))


def main() -> None:
    asteroids = [
        Position(x, y)
        for y, line in enumerate(sys.stdin.readlines())
        for x, c in enumerate(line.rstrip())
        if c == "#"
    ]

    def count_spotted(x: int, y: int) -> int:
        seen: Set[Position] = set()
        ans = 0
        radius = 1

        while True:

            def is_r_away(pos: Position) -> bool:
                return max(abs(pos.x - x), abs(pos.y - y)) == radius

            to_visit = list(filter(is_r_away, asteroids))
            radius += 1
            if len(to_visit) == 0:
                break
            for pos in to_visit:
                rel = (pos.x - x, pos.y - y)
                common = gcd(*rel)
                rel = Position(*(a // common for a in rel))
                if rel in seen:
                    continue  # Already have an asteroid on this path
                seen.add(rel)
                ans += 1

        return ans

    # We need to find the observatory's position as a prerequisite
    ans, orig = max((count_spotted(*pos), pos) for pos in asteroids)
    print(f"({orig.x}, {orig.y}): {ans}")

    def to_rel(p: Position) -> Position:
        return Position(*(a - o for (a, o) in zip(p, orig)))

    angle_dists = sorted(
        (pos_to_angle_dist(to_rel(p)), p) for p in asteroids if p != orig
    )
    grouped_angle_dists = [
        [val[1] for val in group]
        for __, group in groupby(angle_dists, key=lambda x: x[0][0])
    ]

    def find_n_th(n: int) -> Position:
        assert 0 < n < len(asteroids)  # Sanity check
        while n >= len(grouped_angle_dists):
            for group in grouped_angle_dists:
                group.pop(0)
                n -= 1
        return grouped_angle_dists[n - 1][0]

    x, y = find_n_th(200)
    print(x * 100 + y)


if __name__ == "__main__":
    main()
