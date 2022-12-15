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

    def find_hole(intervals: list[Interval], max_coord: int) -> Optional[int]:
        for i in intervals:
            if i.start > 0:
                return i.start - 1
            if i.end < max_coord:
                return i.end + 1

        return None

    def find_sos(data: list[SensorData], max_coord: int) -> Point:
        for row in range(0, max_coord + 1):
            intervals = points_without_sos(data, row)
            if (hole := find_hole(intervals, max_coord)) is not None:
                return Point(hole, row)
        assert False  # Sanity check

    def tuning_frequency(p: Point) -> int:
        return p.x * 4000000 + p.y

    data = [SensorData.from_input(line) for line in input]
    MAX_COORD = 4_000_000
    sos_beacon = find_sos(data, MAX_COORD)
    return tuning_frequency(sos_beacon)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
