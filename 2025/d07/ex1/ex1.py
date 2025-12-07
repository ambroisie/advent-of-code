#!/usr/bin/env python

import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> tuple[Point, set[Point]]:
        start: Point | None = None
        splitters: set[Point] = set()
        for x, line in enumerate(input):
            for y, c in enumerate(line):
                pos = Point(x, y)
                if c == "S":
                    start = pos
                elif c == "^":
                    splitters.add(pos)
        assert start is not None
        return start, splitters

    def run_manifold(start: Point, splitters: set[Point]) -> set[Point]:
        beams = {start}
        current_row = {start.y}
        for x in range(start.x + 1, max(p.x for p in splitters) + 1):
            next_row: set[int] = set()
            for y in current_row:
                p = Point(x, y)
                beams.add(p)
                if p not in splitters:
                    next_row.add(y)
                    continue
                for neighbour in (y - 1, y + 1):
                    beams.add(Point(x, neighbour))
                    next_row.add(neighbour)
            current_row = next_row
        return beams

    start, splitters = parse(input)
    beams = run_manifold(start, splitters)
    return len(beams & splitters)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
