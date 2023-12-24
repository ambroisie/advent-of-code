#!/usr/bin/env python

import sys
from typing import NamedTuple

import z3


class Point(NamedTuple):
    x: int
    y: int
    z: int


class HailStone(NamedTuple):
    pos: Point
    vel: Point


def solve(input: list[str]) -> int:
    def parse_line(line: str) -> HailStone:
        pos, vel = line.split(" @ ")
        return HailStone(
            Point(*map(int, pos.split(", "))), Point(*map(int, vel.split(", ")))
        )

    def parse(input: list[str]) -> list[HailStone]:
        return [parse_line(line) for line in input]

    # Bringing out the big guns to solve this
    def run_z3(hailstones: list[HailStone]) -> HailStone:
        solver = z3.Solver()

        px, py, pz = (z3.Int(f"stone_p{coord}") for coord in ("x", "y", "z"))
        vx, vy, vz = (z3.Int(f"stone_v{coord}") for coord in ("x", "y", "z"))

        for i, other in enumerate(hailstones):
            t = z3.Int(f"t_{i}")
            # Must be in the future
            solver.add(t >= 0)
            # Must hit the hailstone
            solver.add((px + vx * t) == (other.pos.x + other.vel.x * t))
            solver.add((py + vy * t) == (other.pos.y + other.vel.y * t))
            solver.add((pz + vz * t) == (other.pos.z + other.vel.z * t))

        assert solver.check() == z3.sat  # Sanity check

        model = solver.model()
        return HailStone(
            Point(*(model.eval(v).as_long() for v in (px, py, pz))),  # type: ignore
            Point(*(model.eval(v).as_long() for v in (vx, vy, vz))),  # type: ignore
        )

    hailstones = parse(input)
    stone = run_z3(hailstones)
    return sum(stone.pos)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
