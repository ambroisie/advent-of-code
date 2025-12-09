#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> list[Point]:
        return [Point(*map(int, line.split(","))) for line in input]

    def compression_mapping(points: list[Point]) -> dict[Point, Point]:
        def compress_1d(values: set[int]) -> dict[int, int]:
            return {val: i for i, val in enumerate(sorted(values))}

        xs = compress_1d({p.x for p in points})
        ys = compress_1d({p.y for p in points})
        compress = lambda p: Point(xs[p.x], ys[p.y])

        return {p: compress(p) for p in points}

    def line(p1: Point, p2: Point) -> Iterator[Point]:
        def inclusive_range_any_order(a: int, b: int) -> Iterator[int]:
            if a < b:
                yield from range(a, b + 1)
            else:
                yield from range(a, b - 1, -1)

        # Hack-ish work-around to avoid infinite loops
        if p1 == p2:
            yield p1
            return

        xs = inclusive_range_any_order(p1.x, p2.x)
        ys = inclusive_range_any_order(p1.y, p2.y)

        if p1.x == p2.x:
            xs = itertools.repeat(p1.x)

        if p1.y == p2.y:
            ys = itertools.repeat(p1.y)

        yield from map(Point._make, zip(xs, ys))

    def draw_edges(tiles: list[Point]) -> set[Point]:
        # Close the loop by repeating the first vertex at the end
        vertices = tiles + [tiles[0]]
        edges = {p for a, b in itertools.pairwise(vertices) for p in line(a, b)}
        return edges

    def flood_fill(start: Point, points: set[Point]) -> set[Point]:
        assert start in points  # Sanity check
        visited: set[Point] = set()
        stack = [start]
        while stack:
            p = stack.pop()
            visited.add(p)
            for dx, dy in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ):
                n = Point(p.x + dx, p.y + dy)
                if n in visited:
                    continue
                if n not in points:
                    continue
                stack.append(n)
        return visited

    def fill_tiles(tiles: list[Point]) -> set[Point]:
        # I'm too lazy to find an interior point to flood-fill to the edges from,
        # instead fill the exterior and invert the set
        min_x, max_x = min(p.x for p in tiles), max(p.x for p in tiles)
        min_y, max_y = min(p.y for p in tiles), max(p.y for p in tiles)

        # Keep a border all around to make sure the flood-fill can reach everywhere
        all_points = {
            Point(x, y)
            for x in range(min_x - 1, max_x + 1 + 1)
            for y in range(min_y - 1, max_y + 1 + 1)
        }

        edges = draw_edges(tiles)

        # Pick a corner we know for sure won't be in the polygon
        start = Point(min_x - 1, min_y - 1)

        # Sever the points inside and outside the polygon, then flood-fill exterior
        exterior = flood_fill(start, all_points - edges)

        # Return interior/edge points by removing everything that is on the exterior
        return all_points - exterior

    def rectangle_edges(p: Point, other: Point) -> Iterator[Point]:
        min_x, max_x = min(p.x, other.x), max(p.x, other.x)
        min_y, max_y = min(p.y, other.y), max(p.y, other.y)

        c1 = Point(min_x, min_y)
        c2 = Point(max_x, min_y)
        c3 = Point(max_x, max_y)
        c4 = Point(min_x, max_y)

        yield from line(c1, c2)
        yield from line(c2, c3)
        yield from line(c3, c4)
        yield from line(c4, c1)

    def rectangle_area(p: Point, other: Point) -> int:
        dx = abs(p.x - other.x)
        dy = abs(p.y - other.y)
        return (dx + 1) * (dy + 1)

    def inscribed_rectangles(tiles: list[Point]) -> Iterator[tuple[Point, Point]]:
        inside_tiles = fill_tiles(tiles)
        yield from (
            (a, b)
            for a, b in itertools.combinations(tiles, 2)
            if all(p in inside_tiles for p in rectangle_edges(a, b))
        )

    def largest_rectangle_area(tiles: list[Point]) -> int:
        to_compressed = compression_mapping(tiles)
        decompress = {v: k for k, v in to_compressed.items()}.__getitem__
        compressed_tiles = [to_compressed[p] for p in tiles]
        compressed_rectangles = inscribed_rectangles(compressed_tiles)
        return max(
            rectangle_area(decompress(a), decompress(b))
            for a, b in compressed_rectangles
        )

    tiles = parse(input)
    return largest_rectangle_area(tiles)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
