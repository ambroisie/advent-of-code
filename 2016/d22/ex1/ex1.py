#!/usr/bin/env python

import itertools
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Filesystem(NamedTuple):
    size: int
    used: int

    @property
    def avail(self) -> int:
        return self.size - self.used


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[Point, Filesystem]:
        raw_fs, raw_size, raw_used, raw_avail, _ = input.split()
        size = int(raw_size.removesuffix("T"))
        used = int(raw_used.removesuffix("T"))
        avail = int(raw_avail.removesuffix("T"))
        assert size == (used + avail)  # Sanity check
        *_, x, y = raw_fs.split("-")
        return Point(int(x[1:]), int(y[1:])), Filesystem(size, used)

    def parse(input: str) -> dict[Point, Filesystem]:
        return {node: fs for node, fs in map(parse_line, input.splitlines()[2:])}

    df = parse(input)
    return sum(
        a.used <= b.avail
        for a, b in itertools.permutations(df.values(), 2)
        if a.used > 0
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
