#!/usr/bin/env python

import dataclasses
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclasses.dataclass
class Expansion:
    lines: set[int]
    rows: set[int]


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> tuple[list[Point], Expansion]:
        res: list[Point] = []
        expansion = Expansion(set(range(len(input))), set(range(len(input[0]))))

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c != "#":
                    continue
                res.append(Point(x, y))
                expansion.lines.discard(x)
                expansion.rows.discard(y)

        return res, expansion

    def do_expansion(galaxies: list[Point], expansion: Expansion) -> list[Point]:
        new_lines = [0] * len(input)
        new_rows = [0] * len(input[0])

        for i in range(len(new_lines)):
            new_lines[i] = new_lines[i - 1] + (i in expansion.lines) + 1

        for i in range(len(new_rows)):
            new_rows[i] = new_rows[i - 1] + (i in expansion.rows) + 1

        return [Point(new_lines[p.x], new_rows[p.y]) for p in galaxies]

    def dist(a: Point, b: Point) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)

    galaxies, expansion = parse(input)
    galaxies = do_expansion(galaxies, expansion)
    return sum(
        dist(galaxies[i], galaxies[j])
        for i in range(len(galaxies))
        for j in range(i + 1, len(galaxies))
    )


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
