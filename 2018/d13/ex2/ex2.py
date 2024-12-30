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

    def print_state(tracks: dict[Point, Track], carts: list[Cart]) -> None:
        cart_points = {cart.pos: cart for cart in carts}
        max_x, max_y = max(p.x for p in tracks), max(p.y for p in tracks)

        print()
        for x in range(0, max_x + 1):
            for y in range(0, max_y + 1):
                p = Point(x, y)
                if p in cart_points:
                    print(str(cart_points[p].dir), end="")
                elif p in tracks:
                    print(str(tracks[p]), end="")
                else:
                    print(" ", end="")
            print()

    tracks, carts = parse(input.splitlines())
    assert len(carts) % 2 == 1  # Sanity check

    while True:
        cart_positions = {cart.pos for cart in carts}
        crashed: set[Point] = set()
        new_carts: list[Cart] = []
        for cart in carts:
            # Already crashed, nothing to do
            if cart.pos in crashed:
                continue
            new_cart = cart.step(tracks)
            # Is there a crash
            if new_cart.pos in cart_positions:
                cart_positions.remove(new_cart.pos)
                crashed.add(new_cart.pos)
                continue
            cart_positions.remove(cart.pos)
            cart_positions.add(new_cart.pos)
            new_carts.append(new_cart)
        new_carts = [cart for cart in new_carts if cart.pos not in crashed]
        new_carts.sort()
        carts = new_carts
        assert carts  # Sanity check
        if len(carts) == 1:
            return f"{carts[0].pos.y},{carts[0].pos.x}"

    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
