#!/usr/bin/env python

import functools
import itertools
import sys
from typing import Iterator, List, NamedTuple, Optional, Set, Tuple, cast


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Cuboid(NamedTuple):
    min: Point
    max: Point


class Step(NamedTuple):
    state: bool
    bounds: Cuboid


Grid = Set[Cuboid]

MAX_BOUND = 10000000000000000000000000000000000000000000  # Just a very large integer
MIN_BOUND = -MAX_BOUND


def solve(input: List[str]) -> int:
    def parse() -> List[Step]:
        def parse_step(line: str) -> Step:
            state, cuboid = line.split(" ")

            xs, ys, zs = cuboid.split(",")

            min_x, max_x = map(int, xs[2:].split(".."))
            min_y, max_y = map(int, ys[2:].split(".."))
            min_z, max_z = map(int, zs[2:].split(".."))

            # Sanity check
            assert min_x <= max_x
            assert min_y <= max_y
            assert min_z <= max_z

            bounds = Cuboid(Point(min_x, min_y, min_z), Point(max_x, max_y, max_z))

            return Step(state == "on", bounds)

        return [parse_step(line) for line in input]

    def overlapping_range(
        min_a: int, max_a: int, min_b: int, max_b: int
    ) -> Optional[Tuple[int, int]]:
        if max_a < min_b or min_a > max_b:
            return None
        return max(min_a, min_b), min(max_a, max_b)

    def overlapping_cube(cube: Cuboid, other: Cuboid) -> Optional[Cuboid]:
        xs = overlapping_range(cube.min.x, cube.max.x, other.min.x, other.max.x)
        ys = overlapping_range(cube.min.y, cube.max.y, other.min.y, other.max.y)
        zs = overlapping_range(cube.min.z, cube.max.z, other.min.z, other.max.z)

        if xs is None or ys is None or zs is None:
            return None
        return Cuboid(Point(xs[0], ys[0], zs[0]), Point(xs[1], ys[1], zs[1]))

    def overlaps(cube: Cuboid, other: Cuboid) -> bool:
        return overlapping_cube(cube, other) is not None

    def carve_out(grid: Grid, hole: Cuboid) -> Grid:
        from itertools import filterfalse

        def do_carve(c: Cuboid) -> Set[Cuboid]:
            cubes: Set[Cuboid] = set()

            min, max = c

            rightside = overlapping_range(hole.max.x + 1, MAX_BOUND, min.x, max.x)
            leftside = overlapping_range(MIN_BOUND, hole.min.x - 1, min.x, max.x)
            xs = overlapping_range(hole.min.x, hole.max.x, min.x, max.x)
            if rightside is not None:
                min_r, max_r = rightside
                cubes.add(
                    Cuboid(Point(min_r, min.y, min.z), Point(max_r, max.y, max.z))
                )
            if leftside is not None:
                min_l, max_l = leftside
                cubes.add(
                    Cuboid(Point(min_l, min.y, min.z), Point(max_l, max.y, max.z))
                )

            backside = overlapping_range(hole.max.y + 1, MAX_BOUND, min.y, max.y)
            frontside = overlapping_range(MIN_BOUND, hole.min.y - 1, min.y, max.y)
            ys = overlapping_range(hole.min.y, hole.max.y, min.y, max.y)
            if backside is not None and xs is not None:
                min_x, max_x = xs
                min_b, max_b = backside
                cubes.add(
                    Cuboid(Point(min_x, min_b, min.z), Point(max_x, max_b, max.z))
                )
            if frontside is not None and xs is not None:
                min_x, max_x = xs
                min_f, max_f = frontside
                cubes.add(
                    Cuboid(Point(min_x, min_f, min.z), Point(max_x, max_f, max.z))
                )

            topside = overlapping_range(hole.max.z + 1, MAX_BOUND, min.z, max.z)
            bottomside = overlapping_range(MIN_BOUND, hole.min.z - 1, min.z, max.z)
            if topside is not None and xs is not None and ys is not None:
                min_x, max_x = xs
                min_y, max_y = ys
                min_t, max_t = topside
                cubes.add(
                    Cuboid(Point(min_x, min_y, min_t), Point(max_x, max_y, max_t))
                )
            if bottomside is not None and xs is not None and ys is not None:
                min_x, max_x = xs
                min_y, max_y = ys
                min_b, max_b = bottomside
                cubes.add(
                    Cuboid(Point(min_x, min_y, min_b), Point(max_x, max_y, max_b))
                )

            return cubes

        overlaps_us = lambda c: overlaps(c, hole)

        of_interest, other = filter(overlaps_us, grid), filterfalse(overlaps_us, grid)

        return set(other) | set(
            itertools.chain.from_iterable(do_carve(c) for c in of_interest)
        )

    def apply(grid: Grid, step: Step) -> Grid:
        cuboid = step.bounds

        # Remove that cube from the grid, potentially splitting cubes that overlap
        grid = carve_out(grid, cuboid)

        # Add it back in if we want to turn on those cubes
        if step.state:
            grid.add(cuboid)

        return grid

    def count_cubes(c: Cuboid) -> int:
        min, max = c
        return (max.x + 1 - min.x) * (max.y + 1 - min.y) * (max.z + 1 - min.z)

    def score(grid: Grid) -> int:
        area_of_interest = Cuboid(Point(-50, -50, -50), Point(50, 50, 50))
        of_interest = {
            cube
            for cube in map(lambda c: overlapping_cube(c, area_of_interest), grid)
            if cube is not None
        }
        return sum(map(count_cubes, of_interest))

    steps = parse()
    grid: Grid = functools.reduce(apply, steps, set())
    return score(grid)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
