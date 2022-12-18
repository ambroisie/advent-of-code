#!/usr/bin/env python

import sys
from collections.abc import Iterator
from typing import NamedTuple


class Point3(NamedTuple):
    x: int
    y: int
    z: int

    @classmethod
    def from_input(cls, input: str) -> "Point3":
        x, y, z = map(int, input.split(","))
        return cls(x, y, z)

    @classmethod
    def neighbours(cls, p: "Point3") -> Iterator["Point3"]:
        for dx, dy, dz in (
            (0, 0, -1),
            (0, 0, 1),
            (0, -1, 0),
            (0, 1, 0),
            (-1, 0, 0),
            (1, 0, 0),
        ):
            yield cls(p.x + dx, p.y + dy, p.z + dz)


def solve(input: list[str]) -> int:
    cubes = {Point3.from_input(line) for line in input}

    return sum(1 for p in cubes for n in Point3.neighbours(p) if n not in cubes)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
