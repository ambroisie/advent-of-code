#!/usr/bin/env python

import itertools
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
    def compute_unreachable(cubes: set[Point3]) -> set[Point3]:
        def explore(p: Point3, can_reach_out: dict[Point3, bool]) -> bool:
            seen: set[Point3] = set()
            queue: list[Point3] = [p]
            while queue:
                p = queue.pop()
                if p in seen:
                    continue
                if p in can_reach_out:
                    if can_reach_out[p]:
                        return True
                    continue  # Don't go through walls
                seen.add(p)
                queue.extend(Point3.neighbours(p))
            return False

        minx, maxx = min(p.x for p in cubes), max(p.x for p in cubes)
        miny, maxy = min(p.y for p in cubes), max(p.y for p in cubes)
        minz, maxz = min(p.z for p in cubes), max(p.z for p in cubes)

        can_reach_out = {p: False for p in cubes}
        can_reach_out |= {
            Point3(x, y, z): True
            for x, (y, z) in zip(
                itertools.repeat(minx - 1),
                itertools.product(range(miny, maxy + 1), range(minz, maxz + 1)),
            )
        }
        can_reach_out |= {
            Point3(x, y, z): True
            for x, (y, z) in zip(
                itertools.repeat(maxx + 1),
                itertools.product(range(miny, maxy + 1), range(minz, maxz + 1)),
            )
        }
        can_reach_out |= {
            Point3(x, y, z): True
            for y, (x, z) in zip(
                itertools.repeat(miny - 1),
                itertools.product(range(minx, maxx + 1), range(minz, maxz + 1)),
            )
        }
        can_reach_out |= {
            Point3(x, y, z): True
            for y, (x, z) in zip(
                itertools.repeat(maxy + 1),
                itertools.product(range(minx, maxx + 1), range(minz, maxz + 1)),
            )
        }
        can_reach_out |= {
            Point3(x, y, z): True
            for z, (x, y) in zip(
                itertools.repeat(minz - 1),
                itertools.product(range(minx, maxx + 1), range(miny, maxy + 1)),
            )
        }
        can_reach_out |= {
            Point3(x, y, z): True
            for z, (x, y) in zip(
                itertools.repeat(maxz + 1),
                itertools.product(range(minx, maxx + 1), range(miny, maxy + 1)),
            )
        }

        for x, y, z in itertools.product(
            range(minx, maxx + 1),
            range(miny, maxy + 1),
            range(minz, maxz + 1),
        ):
            p = Point3(x, y, z)
            can_reach_out[p] = explore(p, can_reach_out)
        return {p for p, can_reach in can_reach_out.items() if not can_reach}

    cubes = {Point3.from_input(line) for line in input}
    unreachable = compute_unreachable(cubes)

    return sum(1 for p in cubes for n in Point3.neighbours(p) if n not in unreachable)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
