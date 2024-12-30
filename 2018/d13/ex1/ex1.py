#!/usr/bin/env python

import enum
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Track(enum.StrEnum):
    HORIZONTAL = "-"
    VERTICAL = "|"
    TURN = "/"
    ANTI_TURN = "\\"
    INTERSECTION = "+"


class Direction(enum.StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def step(self, p: Point) -> Point:
        dx, dy = {
            Direction.UP: (-1, 0),
            Direction.DOWN: (1, 0),
            Direction.LEFT: (0, -1),
            Direction.RIGHT: (0, 1),
        }[self]
        return Point(p.x + dx, p.y + dy)

    def to_track(self) -> Track:
        if self == Direction.UP or self == Direction.DOWN:
            return Track.VERTICAL
        if self == Direction.LEFT or self == Direction.RIGHT:
            return Track.HORIZONTAL
        assert False  # Sanity check


class IntersectionBehaviour(enum.IntEnum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

    def apply(self, dir: Direction) -> Direction:
        if self == IntersectionBehaviour.STRAIGHT:
            return dir
        if self == IntersectionBehaviour.LEFT:
            return {
                Direction.UP: Direction.LEFT,
                Direction.LEFT: Direction.DOWN,
                Direction.DOWN: Direction.RIGHT,
                Direction.RIGHT: Direction.UP,
            }[dir]
        if self == IntersectionBehaviour.RIGHT:
            return {
                Direction.UP: Direction.RIGHT,
                Direction.RIGHT: Direction.DOWN,
                Direction.DOWN: Direction.LEFT,
                Direction.LEFT: Direction.UP,
            }[dir]
        assert False  # Sanity check

    def next(self) -> "IntersectionBehaviour":
        return IntersectionBehaviour((self + 1) % 3)


class Cart(NamedTuple):
    pos: Point
    dir: Direction
    intersection: IntersectionBehaviour

    def step(self, tracks: dict[Point, Track]) -> "Cart":
        assert self.pos in tracks  # Sanity check
        new_pos = self.dir.step(self.pos)
        track = tracks[new_pos]

        if track in (Track.HORIZONTAL, Track.VERTICAL):
            assert track == self.dir.to_track()  # Sanity check
            return Cart(new_pos, self.dir, self.intersection)
        if track == Track.TURN:
            new_dir = {
                Direction.UP: Direction.RIGHT,
                Direction.DOWN: Direction.LEFT,
                Direction.LEFT: Direction.DOWN,
                Direction.RIGHT: Direction.UP,
            }[self.dir]
            return Cart(new_pos, new_dir, self.intersection)
        if track == Track.ANTI_TURN:
            new_dir = {
                Direction.UP: Direction.LEFT,
                Direction.DOWN: Direction.RIGHT,
                Direction.LEFT: Direction.UP,
                Direction.RIGHT: Direction.DOWN,
            }[self.dir]
            return Cart(new_pos, new_dir, self.intersection)
        if track == Track.INTERSECTION:
            new_dir = self.intersection.apply(self.dir)
            return Cart(new_pos, new_dir, self.intersection.next())
        assert False  # Sanity check


def solve(input: str) -> str:
    def parse(input: list[str]) -> tuple[dict[Point, Track], list[Cart]]:
        tracks: dict[Point, Track] = {}
        carts: list[Cart] = []

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                p = Point(x, y)
                if c in Track:
                    tracks[p] = Track(c)
                elif c in Direction:
                    carts.append(Cart(p, Direction(c), IntersectionBehaviour.LEFT))

        # Don't forget the tracks under the carts
        for cart in carts:
            tracks[cart.pos] = cart.dir.to_track()

        return tracks, carts

    tracks, carts = parse(input.splitlines())

    cart_positions = {cart.pos for cart in carts}
    while True:
        new_carts: list[Cart] = []
        for cart in carts:
            new_cart = cart.step(tracks)
            if new_cart.pos in cart_positions:
                return f"{new_cart.pos.y},{new_cart.pos.x}"
            cart_positions.remove(cart.pos)
            cart_positions.add(new_cart.pos)
            new_carts.append(new_cart)
        new_carts.sort()
        carts = new_carts

    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
