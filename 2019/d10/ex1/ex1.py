#!/usr/bin/env python

import sys
from itertools import chain
from math import gcd
from typing import Set, Tuple

Position = Tuple[int, int]


def main() -> None:
    asteroids = [[c == "#" for c in line.rstrip()] for line in sys.stdin.readlines()]

    def count_spotted(i: int, j: int) -> int:
        def is_valid(pos: Position) -> bool:
            return 0 <= pos[0] < len(asteroids) and 0 <= pos[1] < len(asteroids[0])

        def pos_around(radius: int) -> Set[Position]:
            return set(
                chain(
                    filter(
                        is_valid,
                        (
                            (i - offset, j - radius)
                            for offset in range(-radius, radius + 1)
                        ),
                    ),
                    filter(
                        is_valid,
                        (
                            (i - offset, j + radius)
                            for offset in range(-radius, radius + 1)
                        ),
                    ),
                    filter(
                        is_valid,
                        (
                            (i - radius, j - offset)
                            for offset in range(-radius, radius + 1)
                        ),
                    ),
                    filter(
                        is_valid,
                        (
                            (i + radius, j - offset)
                            for offset in range(-radius, radius + 1)
                        ),
                    ),
                )
            )

        seen: Set[Position] = set()
        ans = 0
        radius = 1
        while asteroids[i][j]:  # Only do this if are on an asteroid
            to_visit = pos_around(radius)
            radius += 1
            if len(to_visit) == 0:
                break
            for pos in to_visit:
                if not asteroids[pos[0]][pos[1]]:
                    continue  # No asteroid there
                rel = (pos[0] - i, pos[1] - j)
                common = gcd(*rel)
                rel = (rel[0] // common, rel[1] // common)
                if rel in seen:
                    continue  # Already have an asteroid on this path
                seen.add(rel)
                ans += 1
        return ans

    ans, y, x = max(
        (count_spotted(i, j), i, j)
        for i in range(len(asteroids))
        for j in range(len(asteroids[0]))
    )
    print(f"({x}, {y}): {ans}")


if __name__ == "__main__":
    main()
