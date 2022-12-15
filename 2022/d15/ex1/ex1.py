#!/usr/bin/env python

import dataclasses
import functools
import sys
from collections.abc import Iterable
from typing import NamedTuple, Optional


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_input(cls, input: str) -> "Point":
        assert input.startswith("x=")  # Sanity check
        x, y = input.split(", ")
        return cls(int(x.split("=")[-1]), int(y.split("=")[-1]))


class Interval(NamedTuple):
    start: int
    end: int

    def as_set(self) -> set[int]:
        return set(range(self.start, self.end + 1))


def merge_intervals(intervals: Iterable[Interval]) -> list[Interval]:
    intervals = sorted(intervals)

    res = [intervals[0]]
    for candidate in intervals[1:]:
        # Range is inclusive in both end, so add 1 to end in case of near miss
        if (res[-1].end + 1) >= candidate.start:
            new_end = max(res[-1].end, candidate.end)
            res[-1] = Interval(res[-1].start, new_end)
        else:
            res.append(candidate)

    return res


def distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


@dataclasses.dataclass
class SensorData:
    pos: Point
    beacon: Point

    @classmethod
    def from_input(cls, input: str) -> "SensorData":
        assert input.startswith("Sensor at x=")  # Sanity check

        mid = input.index(":")
        sensor, beacon = input[:mid], input[mid:]
        return cls(
            Point.from_input(sensor[sensor.index("x") :]),
            Point.from_input(beacon[beacon.index("x") :]),
        )

    @functools.cached_property
    def safe_range(self) -> int:
        return distance(self.pos, self.beacon)

    def scan_row(self, row: int) -> Optional[Interval]:
        distance = abs(row - self.pos.y)
        dx = self.safe_range - distance
        if dx < 0:
            return None
        return Interval(self.pos.x - dx, self.pos.x + dx)


def solve(input: list[str]) -> int:
    def points_without_sos(data: list[SensorData], row: int) -> list[Interval]:
        intervals = (d.scan_row(row) for d in data)
        return merge_intervals(i for i in intervals if i is not None)

    data = [SensorData.from_input(line) for line in input]
    beacons = {d.beacon for d in data}

    ROW = 2_000_000
    intervals = points_without_sos(data, ROW)
    return len(
        set.union(*(i.as_set() for i in intervals))
        - {b.x for b in beacons if b.y == ROW}
    )


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
