#!/usr/bin/env python

import sys
from collections import deque
from collections.abc import Iterator
from enum import Enum, StrEnum
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    NORTH = Point(-1, 0)
    SOUTH = Point(1, 0)
    EAST = Point(0, 1)
    WEST = Point(0, -1)

    def apply(self, pos: Point) -> Point:
        dx, dy = self.value
        return Point(pos.x + dx, pos.y + dy)


class Tile(StrEnum):
    EMPTY = "."
    MIRROR = "/"
    ANTI_MIRROR = "\\"
    VERTICAL_SPLITTER = "|"
    HORIZONTAL_SPLITTER = "-"

    def apply(self, dir: Direction) -> Iterator[Direction]:
        match self:
            case self.EMPTY:
                yield dir
            case self.MIRROR:
                directions = {
                    Direction.EAST: Direction.NORTH,
                    Direction.NORTH: Direction.EAST,
                    Direction.WEST: Direction.SOUTH,
                    Direction.SOUTH: Direction.WEST,
                }
                yield directions[dir]
            case self.ANTI_MIRROR:
                directions = {
                    Direction.WEST: Direction.NORTH,
                    Direction.NORTH: Direction.WEST,
                    Direction.EAST: Direction.SOUTH,
                    Direction.SOUTH: Direction.EAST,
                }
                yield directions[dir]
            case self.VERTICAL_SPLITTER:
                if dir in (Direction.NORTH, Direction.SOUTH):
                    yield dir
                else:
                    yield from (Direction.NORTH, Direction.SOUTH)
            case self.HORIZONTAL_SPLITTER:
                if dir in (Direction.EAST, Direction.WEST):
                    yield dir
                else:
                    yield from (Direction.EAST, Direction.WEST)


class TileMap(NamedTuple):
    tiles: dict[Point, Tile]
    lines: int
    rows: int

    def in_bounds(self, pos: Point) -> bool:
        x, y = pos
        if x < 0 or x >= self.lines:
            return False
        if y < 0 or y >= self.rows:
            return False
        return True


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> TileMap:
        res: dict[Point, Tile] = {}

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                res[Point(x, y)] = Tile(c)

        return TileMap(res, len(input), len(input[0]))

    def compute_energy(map: TileMap, init: tuple[Point, Direction]) -> int:
        queue: deque[tuple[Point, Direction]] = deque([init])
        seen: set[tuple[Point, Direction]] = set()
        energized: set[Point] = set()

        while queue:
            point, dir = queue.popleft()
            if (point, dir) in seen:
                continue
            seen.add((point, dir))
            energized.add(point)
            for new_dir in map.tiles[point].apply(dir):
                new_pos = new_dir.apply(point)
                if not map.in_bounds(new_pos):
                    continue
                queue.append((new_pos, new_dir))

        return len(energized)

    def compute_inits(map: TileMap) -> Iterator[tuple[Point, Direction]]:
        for x in range(map.lines):
            yield (Point(x, 0), Direction.EAST)
            yield (Point(x, map.rows - 1), Direction.WEST)
        for y in range(map.rows):
            yield (Point(0, y), Direction.SOUTH)
            yield (Point(map.lines - 1, y), Direction.NORTH)

    map = parse(input)
    return max(compute_energy(map, init) for init in compute_inits(map))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
