#!/usr/bin/env python

import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def target_coord(target: int) -> Point:
        for dist in itertools.count():
            side = dist * 2 + 1
            bot_right = side * side
            if bot_right < target:
                continue
            # Target must be in the last loop, before bot_right
            bot_left = bot_right - side + 1
            top_left = bot_left - side + 1
            top_right = top_left - side + 1
            if bot_left <= target <= bot_right:
                return Point(dist - (bot_right - target), -dist)
            if top_left <= target <= bot_left:
                return Point(-dist, -dist + (bot_left - target))
            if top_right <= target <= top_left:
                return Point(-dist + (top_left - target), dist)
            if target <= top_right:
                return Point(dist, dist - (top_right - target))
            assert False  # Sanity check
        assert False  # Sanity check

    target = int(input)
    coord = target_coord(target)
    return abs(coord.x) + abs(coord.y)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
