#!/usr/bin/env python

import itertools
import sys
from typing import List, NamedTuple, Set, Tuple


class Point(NamedTuple):
    x: int
    y: int


Algorithm = List[bool]
Image = Set[Point]


def solve(input: List[str]) -> int:
    def parse() -> Tuple[Algorithm, Image]:
        algo_str, blank, *image_str = input

        assert blank == ""  # Sanity check
        assert len(algo_str) == 512  # Sanity check

        algo = [c == "#" for c in algo_str]
        image = {
            Point(i, j)
            for i in range(len(image_str))
            for j in range(len(image_str[0]))
            if image_str[i][j] == "#"
        }

        return algo, image

    def do_step(algo: Algorithm, image: Image, step: int) -> Image:
        min_x, max_x = min(p.x for p in image), max(p.x for p in image)
        min_y, max_y = min(p.y for p in image), max(p.y for p in image)

        def color(p: Point) -> bool:
            # Always return true if we *know* that it is lit
            if p in image:
                return True
            # Return early if the rules don't lead to a flashing infinity case
            flashes_infinity = algo[0] and not algo[-1]
            if not flashes_infinity:
                return False
            # Pixels in proximity to the image are assumed to change their state normally
            if min_x <= p.x <= max_x and min_y <= p.y <= max_y:
                return False
            # Odd indices have a "lit infinity" which turns off, and vice versa
            return (step % 2) == 1

        def bits(p: Point) -> int:
            x, y = p
            res = 0
            for dx, dy in itertools.product(range(-1, 1 + 1), repeat=2):
                res = (res << 1) + color(Point(x + dx, y + dy))
            return res

        # We know the image we care for cannot grow by more than 1 per turn
        xs, ys = range(min_x - 1, max_x + 1 + 1), range(min_y - 1, max_y + 1 + 1)

        res: Image = set()
        for p in map(Point._make, itertools.product(xs, ys)):
            if algo[bits(p)]:
                res.add(p)

        return res

    rules, image = parse()
    for i in range(50):
        image = do_step(rules, image, i)

    return len(image)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
