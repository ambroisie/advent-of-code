#!/usr/bin/env python

import dataclasses
import sys
from collections import defaultdict
from collections.abc import Iterator
from typing import NamedTuple


def sign(x: int) -> int:
    if x == 0:
        return 0
    return 1 if x > 0 else -1


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def fall(self, delta: int = 0) -> "Point":
        assert delta <= self.z  # Sanity check
        return self._replace(z=self.z - delta)


@dataclasses.dataclass
class Brick:
    top_left: Point
    bot_right: Point

    def __post_init__(self) -> None:
        assert self.top_left.z >= self.bot_right.z  # Sanity check

    def orientation(self) -> Point:
        return Point(
            sign(self.bot_right.x - self.top_left.x),
            sign(self.bot_right.y - self.top_left.y),
            sign(self.bot_right.z - self.top_left.z),
        )

    def blocks(self) -> Iterator[Point]:
        p = self.top_left
        dx, dy, dz = self.orientation()
        while p != self.bot_right:
            yield p
            p = Point(p.x + dx, p.y + dy, p.z + dz)
        yield self.bot_right

    def fall(self, delta: int = 0) -> "Brick":
        assert delta >= 0  # Sanity check
        return Brick(self.top_left.fall(delta), self.bot_right.fall(delta))


class TowerMap(NamedTuple):
    supports: dict[int, set[int]]
    supported_by: dict[int, set[int]]
    num_bricks: int

    @classmethod
    def compute_support(cls, tower: dict[Point, int]) -> "TowerMap":
        supports: dict[int, set[int]] = defaultdict(set)
        supported_by: dict[int, set[int]] = defaultdict(set)

        for p, i in tower.items():
            under = p.fall(1)
            support = tower.get(under)
            # No supporting brick
            if support is None:
                continue
            # Don't count the brick as supporting itself
            if support == i:
                continue
            supports[support].add(i)
            supported_by[i].add(support)

        return cls(
            supports=dict(supports),
            supported_by=dict(supported_by),
            num_bricks=max(supports.keys() | supported_by.keys()) + 1,
        )


def solve(input: list[str]) -> int:
    def parse_brick(line: str) -> Brick:
        a, b = (Point._make(map(int, p.split(","))) for p in line.split("~"))
        if a < b:
            a, b = b, a
        return Brick(a, b)

    # Returns which point in space belongs to which brick index
    def drop(snapshots: list[Brick]) -> dict[Point, int]:
        # Re-order by lowest height
        snapshots = sorted(snapshots, key=lambda b: b.bot_right.z)
        # By default the ground is at 0, index with Point(p.x, p.y, 0)
        heights: dict[Point, int] = defaultdict(int)
        res: dict[Point, int] = {}

        for i, brick in enumerate(snapshots):
            z = max(heights[p.fall(p.z)] for p in brick.blocks()) + 1
            assert brick.bot_right.z >= z  # Sanity check
            delta = brick.bot_right.z - z  # Drop it to the top of the pile
            brick = brick.fall(delta)
            # Record the height of the brick for every block composing it
            for p in brick.blocks():
                res[p] = i
                heights[p.fall(p.z)] = brick.top_left.z

        return res

    def can_disintegrate(tower_map: TowerMap, brick: int) -> bool:
        for on_top in tower_map.supports.get(brick, set()):
            if len(tower_map.supported_by[on_top]) == 1:
                return False
        return True

    snapshots = [parse_brick(line) for line in input]
    tower = drop(snapshots)
    tower_map = TowerMap.compute_support(tower)
    return sum(can_disintegrate(tower_map, i) for i in range(tower_map.num_bricks))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
