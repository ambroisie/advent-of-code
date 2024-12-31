#!/usr/bin/env python

import dataclasses
import enum
import heapq
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


class Region(enum.IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2


@dataclasses.dataclass
class Cave:
    depth: int
    target: Point
    erosion: dict[Point, int] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.erosion = {}

    def erosion_at(self, p: Point) -> int:
        if p in self.erosion:
            return self.erosion[p]

        if p == Point(0, 0) or p == self.target:
            self.erosion[p] = 0
        elif p.y == 0:
            self.erosion[p] = p.x * 16807
        elif p.x == 0:
            self.erosion[p] = p.y * 48271
        else:
            self.erosion[p] = self.erosion_at(Point(p.x - 1, p.y)) * self.erosion_at(
                Point(p.x, p.y - 1)
            )
        # Go from geologic index to erosion level
        self.erosion[p] += self.depth
        self.erosion[p] %= 20183
        return self.erosion[p]

    def region_at(self, p: Point) -> Region:
        return Region(self.erosion_at(p) % 3)


class Gear(enum.IntEnum):
    NEITHER = 0
    TORCH = 1
    CLIMBING = 2


class Explorer(NamedTuple):
    pos: Point
    gear: Gear


def solve(input: str) -> int:
    def parse(input: list[str]) -> tuple[int, Point]:
        depth = input[0].removeprefix("depth: ")
        target = input[1].removeprefix("target: ")
        return int(depth), Point(*(int(n) for n in target.split(",")))

    def next_state(explorer: Explorer, cave: Cave) -> Iterator[tuple[int, Explorer]]:
        for n in explorer.pos.neighbours():
            if n.x < 0 or n.y < 0:
                continue
            region = cave.region_at(n)
            if region == Region.ROCKY:
                for gear in (Gear.CLIMBING, Gear.TORCH):
                    yield 1 + (7 if gear != explorer.gear else 0), Explorer(n, gear)
            if region == Region.WET:
                for gear in (Gear.CLIMBING, Gear.NEITHER):
                    yield 1 + (7 if gear != explorer.gear else 0), Explorer(n, gear)
            if region == Region.NARROW:
                for gear in (Gear.TORCH, Gear.NEITHER):
                    yield 1 + (7 if gear != explorer.gear else 0), Explorer(n, gear)

    def djikstra(start: Explorer, end: Explorer, cave: Cave) -> int:
        # Priority queue of (distance, point)
        queue = [(0, start)]
        seen: set[Explorer] = set()

        while len(queue) > 0:
            cost, explorer = heapq.heappop(queue)
            if explorer == end:
                return cost
            # We must have seen p with a smaller distance before
            if explorer in seen:
                continue
            # First time encountering p, must be the smallest distance to it
            seen.add(explorer)
            # Add all neighbours to be visited
            for time, n in next_state(explorer, cave):
                heapq.heappush(queue, (cost + time, n))

        assert False  # Sanity check

    depth, target = parse(input.splitlines())
    cave = Cave(depth, target)
    start = Explorer(Point(0, 0), Gear.TORCH)
    end = Explorer(target, Gear.TORCH)
    return djikstra(start, end, cave)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
