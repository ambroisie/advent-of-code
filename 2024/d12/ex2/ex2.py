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


def solve(input: str) -> int:
    def parse(input: list[str]) -> dict[Point, str]:
        return {
            Point(x, y): c for x, line in enumerate(input) for y, c in enumerate(line)
        }

    def find_plots(garden: dict[Point, str]) -> list[set[Point]]:
        res: list[set[Point]] = []
        visited: set[Point] = set()

        for p, plant in garden.items():
            if p in visited:
                continue
            plot: set[Point] = set()
            to_visit = {p}
            while to_visit:
                p = to_visit.pop()
                visited.add(p)
                plot.add(p)
                assert garden[p] == plant  # Sanity check
                for n in p.neighbours():
                    if garden.get(n) != plant:
                        continue
                    if n in visited:
                        continue
                    to_visit.add(n)
            res.append(plot)
        return res

    def count_corners(plot: set[Point]) -> int:
        def corners(p: Point) -> int:
            res = 0
            for dx, dy in (
                (-1, -1),
                (1, 1),
                (-1, 1),
                (1, -1),
            ):
                diag = Point(p.x + dx, p.y + dy)
                vert = Point(p.x + dx, p.y)
                hori = Point(p.x, p.y + dy)
                # Both sides are out: an outside corner
                if vert not in plot and hori not in plot:
                    res += 1
                # Both sides are in, diagonal is out: an inside corner
                if vert in plot and hori in plot and diag not in plot:
                    res += 1
            return res

        return sum(corners(p) for p in plot)

    def fence_price(plot: set[Point]) -> int:
        area = len(plot)
        # Number of sides is equal to number of corners
        sides = count_corners(plot)
        return area * sides

    garden = parse(input.splitlines())
    plots = find_plots(garden)
    return sum(map(fence_price, plots))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
