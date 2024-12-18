#!/usr/bin/env python

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


DIMS = Point(70, 70)


def solve(input: str) -> str:
    def parse(input: list[str]) -> list[Point]:
        return [Point(*map(int, line.split(","))) for line in input]

    def djikstra(start: Point, end: Point, blocks: set[Point]) -> int | None:
        # Priority queue of (distance, point)
        queue = [(0, start)]
        seen: set[Point] = set()

        while len(queue) > 0:
            cost, p = heapq.heappop(queue)
            if p == end:
                return cost
            # We must have seen p with a smaller distance before
            if p in seen:
                continue
            # First time encountering p, must be the smallest distance to it
            seen.add(p)
            # Add all neighbours to be visited
            for n in p.neighbours():
                if p in blocks:
                    continue
                if not 0 <= p.x <= DIMS.x:
                    continue
                if not 0 <= p.y <= DIMS.y:
                    continue
                heapq.heappush(queue, (cost + 1, n))

        return None

    def bisect_cutoff(start: Point, end: Point, blocks: list[Point]) -> Point:
        # Cutting off the path is monotonic: once cut-off, it's never uncut
        low, high = 0, len(blocks)
        while low < high:
            mid = low + (high - low) // 2
            if djikstra(start, end, set(blocks[: mid + 1])) is None:
                high = mid
            else:
                low = mid + 1
        return blocks[low]

    coords = parse(input.splitlines())
    byte = bisect_cutoff(Point(0, 0), DIMS, coords)
    return f"{byte.x},{byte.y}"


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
