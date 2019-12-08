#!/usr/bin/env python

import sys
from fractions import Fraction
from typing import Dict, List, NamedTuple, Optional


class Point(NamedTuple):
    x: int
    y: int


class Line(NamedTuple):
    p1: Point
    p2: Point


def manhattan_dist(p1: Point, p2: Point = Point(0, 0)) -> int:
    dx = p2.x - p1.x if p1.x < p2.x else p1.x - p2.x
    dy = p2.y - p1.y if p1.y < p2.y else p1.y - p2.y
    return dx + dy


def intersect(l1: Line, l2: Line) -> Optional[Point]:
    (x1, y1), (x2, y2) = l1.p1, l1.p2
    (x3, y3), (x4, y4) = l2.p1, l2.p2

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if den == 0:  # Parallel lines
        return None

    t = Fraction((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4), den)
    if t < 0 or t > 1:  # Out of l1
        return None

    u = -Fraction((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3), den)
    if u < 0 or u > 1:  # Out of l2
        return None

    dx = t * (x2 - x1)
    dy = t * (y2 - y1)

    assert int(dx) == dx and int(dy) == dy  # Sanity checks

    ix = x1 + int(dx)
    iy = y1 + int(dy)
    return Point(ix, iy)


def is_on(p: Point, l: Line) -> bool:
    # Assume that l is horizontal or vertical
    if l.p1.x == l.p2.x:
        if l.p1.y < l.p2.y:
            return p.x == l.p1.x and l.p1.y <= p.y <= l.p2.y
        elif l.p2.y < l.p1.y:
            return p.x == l.p1.x and l.p2.y <= p.y <= l.p1.y
    elif l.p1.y == l.p2.y:
        if l.p1.x < l.p2.x:
            return p.y == l.p1.y and l.p1.x <= p.x <= l.p2.x
        elif l.p2.x < l.p1.x:
            return p.y == l.p1.y and l.p2.x <= p.x <= l.p1.x
    assert False  # Sanity checks


def parse_line(directions: str) -> List[Line]:
    prev = Point(0, 0)
    ans = []
    for inst in directions.split(","):
        direction, length = inst[0], int(inst[1:])
        new_x, new_y = prev
        if direction == "U":
            new_y += length
        elif direction == "R":
            new_x += length
        if direction == "D":
            new_y -= length
        elif direction == "L":
            new_x -= length
        new = Point(new_x, new_y)
        ans.append(Line(prev, new))
        prev = new
    return ans


def compute_delay(p: Point, lines: List[Line]) -> int:
    dist = 0
    for l in lines:
        if is_on(p, l):
            return dist + manhattan_dist(l.p1, p)
        dist += manhattan_dist(l.p1, l.p2)
    assert False  # Sanity check


def main() -> None:
    wire1, wire2 = tuple(parse_line(l) for l in sys.stdin)
    intersections = [intersect(l1, l2) for l1 in wire1 for l2 in wire2]
    print(
        min(
            compute_delay(x, wire1) + compute_delay(x, wire2)
            for x in intersections
            if x is not None and x != Point(0, 0)  # Discard origin
        )
    )


if __name__ == "__main__":
    main()
