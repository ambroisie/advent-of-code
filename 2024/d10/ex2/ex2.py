#!/usr/bin/env python

import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def neighbours(self) -> Iterator["Point"]:
        for dx, dy in (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ):
            yield Point(self.x + dx, self.y + dy)


TopoMap = dict[Point, int]


def solve(input: str) -> int:
    def parse(input: list[str]) -> TopoMap:
        return {
            Point(x, y): int(c)
            for x, line in enumerate(input)
            for y, c in enumerate(line)
        }

    def find_trail_heads(map: TopoMap) -> set[Point]:
        return {p for p, height in map.items() if height == 0}

    def rate_trail(map: TopoMap, start: Point) -> int:
        def helper(pos: Point) -> int:
            if map[pos] == 9:
                return 1
            res = 0
            for n in pos.neighbours():
                if map.get(n, -1) != (map[pos] + 1):
                    continue
                res += helper(n)
            return res

        assert map[start] == 0  # Sanity check
        return helper(start)

    map = parse(input.splitlines())
    trail_heads = find_trail_heads(map)
    return sum(rate_trail(map, head) for head in sorted(trail_heads))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
