#!/usr/bin/env python

import itertools
import sys
from collections import Counter
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Claim(NamedTuple):
    top_left: Point
    size: Point

    def points(self) -> Iterator[Point]:
        for dx, dy in map(
            Point._make, itertools.product(range(self.size.x), range(self.size.y))
        ):
            yield Point(self.top_left.x + dx, self.top_left.y + dy)


def solve(input: str) -> int:
    def parse_claim(input: str) -> Claim:
        offset, size = input.split("@")[1].strip().split(": ")
        return Claim(
            Point(*map(int, offset.split(","))),
            Point(*map(int, size.split("x"))),
        )

    def parse(input: list[str]) -> list[Claim]:
        return [parse_claim(line) for line in input]

    def claim_per_point(claims: list[Claim]) -> dict[Point, int]:
        points = itertools.chain.from_iterable(map(Claim.points, claims))
        return Counter(points)

    claims = parse(input.splitlines())
    return sum(count > 1 for count in claim_per_point(claims).values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
