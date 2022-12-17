#!/usr/bin/env python

import enum
import itertools
import sys
from collections.abc import Iterator
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


def translate(points: set[Point], delta: Point) -> set[Point]:
    return {p + delta for p in points}


class Rock(str, enum.Enum):
    LINE = "####"
    PLUS = ".#.\n###\n.#."
    CORNER = "..#\n..#\n###"
    VERTICAL_LINE = "#\n#\n#\n#"
    SQUARE = "##\n##"

    @classmethod
    def stream(cls) -> Iterator["Rock"]:
        yield from itertools.cycle(iter(cls))

    def to_points(self) -> set[Point]:
        res: set[Point] = set()

        for y, line in enumerate(reversed(self.splitlines())):
            for x, c in enumerate(line):
                if c == ".":
                    continue
                res.add(Point(x, y))

        return res


class JetStream(str, enum.Enum):
    LEFT = "<"
    RIGHT = ">"

    @classmethod
    def stream(cls, jet_pattern: str) -> Iterator["JetStream"]:
        yield from itertools.cycle(map(cls, jet_pattern))

    def as_delta(self) -> Point:
        if self == self.LEFT:
            return Point(-1, 0)
        if self == self.RIGHT:
            return Point(1, 0)
        assert False  # Sanity check


def solve(input: list[str]) -> int:
    fallen_stack: set[Point] = set()
    max_height = 0

    LEFT_WALL = -1
    RIGHT_WALL = 7
    FLOOR = 0

    rocks = list(iter(Rock))
    jet_stream = [JetStream(c) for c in input[0]]

    t = 0
    jet_index = 0
    rock_index = 0

    def step(rock: set[Point], jet: JetStream) -> tuple[set[Point], bool]:
        # Check if it can be pushed by the jet, or if it hits an obstacle
        pushed_rock = translate(rock, jet.as_delta())
        if not (fallen_stack & pushed_rock) and all(
            LEFT_WALL < p.x < RIGHT_WALL for p in pushed_rock
        ):
            rock = pushed_rock

        # Check if it can go down
        fallen_rock = translate(rock, Point(0, -1))

        if not (fallen_stack & fallen_rock) and all(p.y > FLOOR for p in fallen_rock):
            return fallen_rock, True
        return rock, False

    def simulate_rock_fall() -> None:
        nonlocal max_height
        nonlocal jet_index
        nonlocal rock_index

        rock = rocks[rock_index].to_points()

        # Align 2 units away from LEFT_WALL and 3 higher than
        # current stack
        rock = translate(rock, Point(2, max_height + 3 + 1))

        while True:
            rock, keep_going = step(rock, jet_stream[jet_index])
            jet_index = (jet_index + 1) % len(jet_stream)
            if not keep_going:
                break

        fallen_stack.update(rock)
        max_height = max(max_height, max(p.y for p in rock))
        rock_index = (rock_index + 1) % len(rocks)

    StackStateHash = tuple[int, int, frozenset[Point]]

    def stack_state_hash() -> StackStateHash:
        top = frozenset(
            Point(p.x, p.y - max_height)
            for p in fallen_stack
            if p.y >= (max_height - 50)  # Cut-off point chosen arbitrarily...
        )
        return rock_index, jet_index, top

    assert len(input) == 1  # Sanity check

    cache: dict[StackStateHash, tuple[int, int]] = {}
    added_height = 0

    END_OF_SIMULATION = 1_000_000_000_000
    while t < END_OF_SIMULATION:
        simulate_rock_fall()
        t += 1
        stack_hash = stack_state_hash()
        if stack_hash in cache:
            previous_t, previous_height = cache[stack_hash]
            cycle_length = t - previous_t
            num_cycles = (END_OF_SIMULATION - t) // cycle_length
            added_height += num_cycles * (max_height - previous_height)
            t += num_cycles * cycle_length
        else:
            cache[stack_hash] = t, max_height

    return max_height + added_height


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
