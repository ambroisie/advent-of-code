#!/usr/bin/env python

import itertools
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


class ParsedMap(NamedTuple):
    start: Point
    end: Point
    tracks: set[Point]


MIN_SAVE = 100


def solve(input: str) -> int:
    def parse(input: list[str]) -> ParsedMap:
        start: Point | None = None
        end: Point | None = None
        tracks: set[Point] = set()

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == "#":
                    continue
                p = Point(x, y)
                if c == "S":
                    start = p
                elif c == "E":
                    end = p
                tracks.add(p)

        assert start is not None and end is not None  # Sanity check
        return ParsedMap(start, end, tracks)

    def flood_distance(start: Point, points: set[Point]) -> dict[Point, int]:
        res = {start: 0}
        queue = {start}

        while queue:
            p = queue.pop()
            dist = res[p]
            for n in p.neighbours():
                if n in res:
                    continue
                if n not in points:
                    continue
                res[n] = dist + 1
                queue.add(n)

        return res

    def dist(a: Point, b: Point) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)

    def disk(p: Point, radius: int) -> Iterator[Point]:
        for dx, dy in itertools.product(range(-radius, radius + 1), repeat=2):
            n = Point(p.x + dx, p.y + dy)
            if dist(p, n) > radius:
                continue
            yield n

    def find_cheats(start: Point, end: Point, tracks: set[Point]) -> int:
        start_dist = flood_distance(start, tracks)
        end_dist = flood_distance(end, tracks)

        assert start_dist[end] == end_dist[start]
        fastest = start_dist[end]

        res = 0
        for a in tracks:
            for b in disk(a, 20):
                if b not in tracks:
                    continue
                time = start_dist[a] + dist(a, b) + end_dist[b]
                if (fastest - time) < MIN_SAVE:
                    continue
                res += 1
        return res

    start, end, tracks = parse(input.splitlines())
    return find_cheats(start, end, tracks)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
