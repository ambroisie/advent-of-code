#!/usr/bin/env python

import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int


class NanoBot(NamedTuple):
    pos: Point
    r: int


def solve(input: str) -> int:
    def parse_nanobot(input: str) -> NanoBot:
        pos, r = input.split(", ")
        pos = pos.removeprefix("pos=<").removesuffix(">")
        r = r.removeprefix("r=")
        return NanoBot(Point(*(int(n) for n in pos.split(","))), int(r))

    def parse(input: list[str]) -> list[NanoBot]:
        return [parse_nanobot(line) for line in input]

    def dist(lhs: Point, rhs: Point) -> int:
        return sum(abs(l - r) for l, r in zip(lhs, rhs))

    bots = parse(input.splitlines())
    strongest = max(bots, key=lambda b: b.r)
    return sum(dist(strongest.pos, bot.pos) <= strongest.r for bot in bots)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
