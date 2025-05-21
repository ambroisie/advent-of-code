#!/usr/bin/env python

import sys
from typing import NamedTuple


class Sue(NamedTuple):
    children: int | None = None
    cats: int | None = None
    samoyeds: int | None = None
    pomeranians: int | None = None
    akitas: int | None = None
    vizslas: int | None = None
    goldfish: int | None = None
    trees: int | None = None
    cars: int | None = None
    perfumes: int | None = None

    def matches(self, reading: dict[str, int | None]) -> bool:
        for name, expected in reading.items():
            assert expected is not None  # Sanity check
            val = getattr(self, name)
            if name in ("cats", "trees"):
                if val is not None and val <= expected:
                    return False
            elif name in ("pomeranians", "goldfish"):
                if val is not None and val >= expected:
                    return False
            else:
                if val is not None and val != expected:
                    return False
        return True


def solve(input: str) -> int:
    def parse_line(input: str) -> Sue:
        _, other = input.split(": ", 1)
        raw_items = other.split(", ")
        items = {
            name: int(val) for name, val in (item.split(": ") for item in raw_items)
        }
        return Sue(**items)

    def parse(input: str) -> list[Sue]:
        return [parse_line(line) for line in input.splitlines()]

    aunts = parse(input)
    reading = Sue(
        children=3,
        cats=7,
        samoyeds=2,
        pomeranians=3,
        akitas=0,
        vizslas=0,
        goldfish=5,
        trees=3,
        cars=2,
        perfumes=1,
    )
    return next(i for i, sue in enumerate(aunts, 1) if sue.matches(reading._asdict()))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
