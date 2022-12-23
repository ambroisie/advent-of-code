#!/usr/bin/env python

import itertools
import sys
from collections import defaultdict, deque
from collections.abc import Iterator, Sequence
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)


ElfMap = set[Point]


def neighbours(p: Point) -> Iterator[Point]:
    for dx, dy in itertools.product(range(-1, 1 + 1), repeat=2):
        if dx == 0 and dy == 0:
            continue
        yield p + Point(dx, dy)


class MoveCandidate(NamedTuple):
    dir: Point
    empties: set[Point]


MOVES = [
    # North
    MoveCandidate(Point(-1, 0), {Point(-1, -1), Point(-1, 0), Point(-1, 1)}),
    # South
    MoveCandidate(Point(1, 0), {Point(1, -1), Point(1, 0), Point(1, 1)}),
    # West
    MoveCandidate(Point(0, -1), {Point(-1, -1), Point(0, -1), Point(1, -1)}),
    # East
    MoveCandidate(Point(0, 1), {Point(-1, 1), Point(0, 1), Point(1, 1)}),
]


def solve(input: list[str]) -> int:
    def to_map(input: list[str]) -> ElfMap:
        res: ElfMap = set()
        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c != "#":
                    continue
                res.add(Point(x, y))
        return res

    def do_round(map: ElfMap, moves: Sequence[MoveCandidate]) -> ElfMap:
        move: dict[Point, Point] = {elf: elf for elf in map}
        dest_count: dict[Point, int] = defaultdict(int)
        # Consider destinations all at once
        for elf in map:
            if not any(n in map for n in neighbours(elf)):
                continue
            for candidate in iter(moves):
                if any((elf + delta) in map for delta in candidate.empties):
                    continue
                dest = elf + candidate.dir
                move[elf] = dest
                dest_count[dest] += 1
                break
        # Only move elves that don't overlap
        res: ElfMap = set()
        for elf, dest in move.items():
            if dest_count[dest] > 1:
                res.add(elf)
            else:
                res.add(dest)
        assert len(res) == len(map)  # Sanity check
        return res

    map = to_map(input)
    moves = deque(MOVES)
    i = 1
    while (new_map := do_round(map, moves)) != map:
        map = new_map
        moves.rotate(-1)
        i += 1
    return i


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
