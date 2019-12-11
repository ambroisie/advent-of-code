#!/usr/bin/env python

import sys
from math import gcd
from typing import NamedTuple, Set


class Position(NamedTuple):
    x: int
    y: int


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

    ans, x, y = max((count_spotted(*pos), *pos) for pos in asteroids)
    print(f"({x}, {y}): {ans}")


if __name__ == "__main__":
    main()
