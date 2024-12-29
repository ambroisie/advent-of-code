#!/usr/bin/env python

import itertools
import sys
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

    def claims_overlap(claim: Claim, other: Claim) -> bool:
        min_x1, min_y1 = claim.top_left
        max_x1, max_y1 = map(sum, zip(claim.top_left, claim.size))
        min_x2, min_y2 = other.top_left
        max_x2, max_y2 = map(sum, zip(other.top_left, other.size))

        return (
            True
            and (min_x2 < max_x1 and min_x1 < max_x2)
            and (min_y2 < max_y1 and min_y1 < max_y2)
        )

    def find_non_overlapping(claims: list[Claim]) -> int:
        for i, claim in enumerate(claims):
            overlaps = any(
                claims_overlap(claim, other) for j, other in enumerate(claims) if i != j
            )
            if not overlaps:
                return i + 1  # They use 1-based indexing
        assert False  # Sanity check

    claims = parse(input.splitlines())
    return find_non_overlapping(claims)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
