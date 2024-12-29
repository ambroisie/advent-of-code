#!/usr/bin/env python

import itertools
import sys
from collections import Counter, defaultdict
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def parse(input: list[str]) -> list[Point]:
        return [Point(*map(int, line.split(", "))) for line in input]

    def dist(lhs: Point, rhs: Point) -> int:
        return sum(abs(a - b) for a, b in zip(lhs, rhs))

    def points_distances(coords: list[Point]) -> dict[Point, Counter[Point]]:
        top_left = Point(min(p.x for p in coords), min(p.y for p in coords))
        bot_right = Point(max(p.x for p in coords), max(p.y for p in coords))

        return {
            p: Counter({root: dist(root, p) for root in coords})
            for p in map(
                Point._make,
                itertools.product(
                    range(top_left.x, bot_right.x + 1),
                    range(top_left.y, bot_right.y + 1),
                ),
            )
        }

    def remove_areas_on_border(
        areas: dict[Point, set[Point]],
        top_left: Point,
        bot_right: Point,
    ) -> dict[Point, set[Point]]:
        def on_border(points: set[Point]) -> bool:
            return any(
                p.x in (top_left.x, bot_right.x) or p.y in (top_left.y, bot_right.y)
                for p in points
            )

        return {root: points for root, points in areas.items() if not on_border(points)}

    def points_areas(coords: list[Point]) -> dict[Point, int]:
        top_left = Point(min(p.x for p in coords), min(p.y for p in coords))
        bot_right = Point(max(p.x for p in coords), max(p.y for p in coords))

        distances = points_distances(coords)
        areas: dict[Point, set[Point]] = defaultdict(set)
        for p, root_distances in distances.items():
            closest, dist = root_distances.most_common()[-1]
            if dist == root_distances.most_common()[-2][1]:
                continue
            areas[closest].add(p)

        areas = remove_areas_on_border(areas, top_left, bot_right)
        return {root: len(points) for root, points in areas.items()}

    coords = parse(input.splitlines())
    areas = points_areas(coords)
    return max(areas.values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
