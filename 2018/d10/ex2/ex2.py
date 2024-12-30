#!/usr/bin/env python

import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Light(NamedTuple):
    pos: Point
    vel: Point

    def at(self, time: int) -> Point:
        return Point(self.pos.x + self.vel.x * time, self.pos.y + self.vel.y * time)


def solve(input: str) -> int:
    def parse_light(input: str) -> Light:
        pos, vel = map(lambda s: s.split("=<")[1].removesuffix(">"), input.split("> "))
        return Light(
            Point(*map(int, map(str.strip, pos.split(",")))),
            Point(*map(int, map(str.strip, vel.split(",")))),
        )

    def parse(input: list[str]) -> list[Light]:
        return [parse_light(line) for line in input]

    def move_lights(lights: list[Light], time: int) -> set[Point]:
        return {l.at(time) for l in lights}

    def bbox_size(points: set[Point]) -> int:
        min_x, max_x = min(p.x for p in points), max(p.x for p in points)
        min_y, max_y = min(p.y for p in points), max(p.y for p in points)
        return (max_x - min_x + 1) * (max_y - min_y + 1)

    def write_message(message: set[Point]) -> str:
        min_x, max_x = min(p.x for p in message), max(p.x for p in message)
        min_y, max_y = min(p.y for p in message), max(p.y for p in message)

        return "\n".join(
            "".join(
                "#" if Point(x, y) in message else "." for x in range(min_x, max_x + 1)
            )
            for y in range(min_y, max_y + 1)
        )

    lights = parse(input.splitlines())
    max_time = max(
        map(abs, itertools.chain.from_iterable((l.pos.x, l.pos.y) for l in lights))
    )
    time = min(range(max_time), key=lambda t: bbox_size(move_lights(lights, t)))
    return time


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
