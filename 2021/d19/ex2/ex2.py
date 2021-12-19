#!/usr/bin/env python

import functools
import itertools
import sys
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple


@dataclass(eq=True, frozen=True)  # Hash-able
class Vector:
    x: int
    y: int
    z: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)


@dataclass(eq=True, frozen=True)  # Hash-able
class Matrix:
    v1: Vector
    v2: Vector
    v3: Vector

    def __matmul__(self, other: Vector) -> Vector:
        return Vector(
            self.v1.x * other.x + self.v1.y * other.y + self.v1.z * other.z,
            self.v2.x * other.x + self.v2.y * other.y + self.v2.z * other.z,
            self.v3.x * other.x + self.v3.y * other.y + self.v3.z * other.z,
        )


def rotations() -> List[Matrix]:
    def cos(angle: int) -> int:
        if angle == 0:
            return 1
        if angle == 180:
            return -1
        assert angle in (90, 270)  # Sanity check
        return 0

    def sin(angle: int) -> int:
        if angle == 90:
            return 1
        if angle == 270:
            return -1
        assert angle in (0, 180)  # Sanity check
        return 0

    def rotate(x: int, y: int, z: int) -> Matrix:
        v1 = Vector(
            cos(z) * cos(y),
            cos(z) * sin(y) * sin(x) - sin(z) * cos(x),
            cos(z) * sin(y) * cos(x) + sin(z) * sin(x),
        )
        v2 = Vector(
            sin(z) * cos(y),
            sin(z) * sin(y) * sin(x) + cos(z) * cos(x),
            sin(z) * sin(y) * cos(x) - cos(z) * sin(x),
        )
        v3 = Vector(-sin(y), cos(y) * sin(x), cos(y) * cos(x))
        return Matrix(v1, v2, v3)

    return [
        rotate(0, 0, 0),
        rotate(90, 0, 0),
        rotate(180, 0, 0),
        rotate(270, 0, 0),
        rotate(0, 90, 0),
        rotate(90, 90, 0),
        rotate(180, 90, 0),
        rotate(270, 90, 0),
        rotate(0, 180, 0),
        rotate(90, 180, 0),
        rotate(180, 180, 0),
        rotate(270, 180, 0),
        rotate(0, 270, 0),
        rotate(90, 270, 0),
        rotate(180, 270, 0),
        rotate(270, 270, 0),
        rotate(0, 0, 90),
        rotate(90, 0, 90),
        rotate(180, 0, 90),
        rotate(270, 0, 90),
        rotate(0, 0, 270),
        rotate(90, 0, 270),
        rotate(180, 0, 270),
        rotate(270, 0, 270),
    ]


ROTATIONS = rotations()

BeaconList = Set[Vector]


def solve(input: List[str]) -> int:
    def parse() -> List[BeaconList]:
        res: List[BeaconList] = []

        for line in input:
            if "scanner" in line:
                res.append(set())
                continue
            if line == "":
                continue
            x, y, z = map(int, line.split(","))
            res[-1].add(Vector(x, y, z))

        return res

    def find_overlap(
        known: BeaconList, other: BeaconList
    ) -> Optional[Tuple[Matrix, Vector]]:
        def find_delta(known: BeaconList, other: BeaconList) -> Optional[Vector]:
            for dest, source in itertools.product(known, rotated):
                delta = dest - source
                if sum((v + delta) in known for v in rotated) >= 12:
                    return delta
            return None

        for r in ROTATIONS:
            rotated = set(r @ v for v in other)
            if (delta := find_delta(known, rotated)) is not None:
                return r, delta

        return None

    def apply(known: BeaconList, other: BeaconList) -> Tuple[bool, Vector, BeaconList]:
        res = find_overlap(known, other)
        if res is None:
            return False, Vector(0, 0, 0), known

        rot, delta = res

        new = {(rot @ v) + delta for v in other}

        # Return whether there are new points in the set
        return (new <= known), delta, (known | new)

    def match_all(scans: List[BeaconList]) -> Set[Vector]:
        # First scan is our basis
        known = scans[0]
        # No need to inspect the first scan in the future
        to_match = scans[1:]
        # Position our first scanner at the origin
        deltas = {Vector(0, 0, 0)}

        while to_match:
            s = to_match.pop(0)
            applied, delta, known = apply(known, s)
            if not applied:
                to_match.append(s)
            else:
                deltas.add(delta)
        return deltas

    def manhattan_dist(v1: Vector, v2: Vector) -> int:
        return abs(v1.x - v2.x) + abs(v1.y - v2.y) + abs(v1.z - v2.z)

    beacons = parse()
    scanner_positions = match_all(beacons)
    return max(
        manhattan_dist(v1, v2)
        for v1, v2 in itertools.combinations(scanner_positions, 2)
    )


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
