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

    def fence_price(plot: set[Point]) -> int:
        area = len(plot)
        perimeter = sum(n not in plot for p in plot for n in p.neighbours())
        return area * perimeter

    garden = parse(input.splitlines())
    plots = find_plots(garden)
    return sum(map(fence_price, plots))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
