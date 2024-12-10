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

    def score_trail(map: TopoMap, start: Point) -> int:
        assert map[start] == 0  # Sanity check
        res = 0
        queue = {start}
        visited: set[Point] = set()
        while queue:
            p = queue.pop()
            visited.add(p)
            cur_height = map[p]
            if cur_height == 9:
                res += 1
            for n in p.neighbours():
                if map.get(n, cur_height) != (cur_height + 1):
                    continue
                if n in visited:
                    continue
                queue.add(n)
        return res

    map = parse(input.splitlines())
    trail_heads = find_trail_heads(map)
    return sum(score_trail(map, head) for head in sorted(trail_heads))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
