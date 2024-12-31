#!/usr/bin/env python

import sys
from typing import NamedTuple

import z3


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

    def find_best(bots: list[NanoBot]) -> Point:
        def z3_abs(n: z3.ArithRef) -> z3.ArithRef:
            return z3.If(n > 0, n, -n)  # type: ignore

        def z3_dist(lhs: tuple[z3.ArithRef, ...], rhs: Point) -> z3.ArithRef:
            return sum(z3_abs(l - r) for l, r in zip(lhs, rhs))  # type: ignore

        pos = tuple(z3.Int(c) for c in ("x", "y", "z"))

        in_range = [z3.Int(f"in_range_{i}") for i in range(len(bots))]
        total = z3.Int("total")
        optimizer = z3.Optimize()

        for i, bot in enumerate(bots):
            optimizer.add(in_range[i] == (z3_dist(pos, bot.pos) <= bot.r))
        optimizer.add(total == sum(in_range))

        dist_to_origin = z3.Int("dist_to_origin")
        optimizer.add(dist_to_origin == z3_dist(pos, Point(0, 0, 0)))

        optimizer.maximize(total)
        optimizer.minimize(dist_to_origin)

        assert optimizer.check() == z3.sat  # Sanity check
        model = optimizer.model()

        return Point(*(map(lambda v: model.eval(v).as_long(), pos)))  # type: ignore

    bots = parse(input.splitlines())
    return dist(find_best(bots), Point(0, 0, 0))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
