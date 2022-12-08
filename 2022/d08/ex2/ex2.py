#!/usr/bin/env python

import dataclasses
import sys
from collections.abc import Iterator


@dataclasses.dataclass
class Point:
    x: int
    y: int


def solve(input: list[list[int]]) -> int:
    def up(p: Point) -> Iterator[Point]:
        x = p.x
        while (x := x - 1) >= 0:
            yield Point(x, p.y)

    def down(p: Point) -> Iterator[Point]:
        x = p.x
        while (x := x + 1) < len(input):
            yield Point(x, p.y)

    def left(p: Point) -> Iterator[Point]:
        y = p.y
        while (y := y - 1) >= 0:
            yield Point(p.x, y)

    def right(p: Point) -> Iterator[Point]:
        y = p.y
        while (y := y + 1) < len(input[0]):
            yield Point(p.x, y)

    def visible_trees(p: Point, neighbours: Iterator[Point]) -> Iterator[Point]:
        height = input[p.x][p.y]
        for n in neighbours:
            yield n
            if height <= input[n.x][n.y]:
                break

    def score(p: Point) -> int:
        score = 1
        for neighbours in (up, down, left, right):
            score *= len(list(visible_trees(p, neighbours(p))))
        return score

    scores = [
        [score(Point(x, y)) for y in range(len(input[x]))] for x in range(len(input))
    ]
    return max(map(max, scores))


def main() -> None:
    input = [[int(c) for c in line] for line in sys.stdin.read().splitlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
