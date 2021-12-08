#!/usr/bin/env python

import itertools
import sys
from dataclasses import dataclass
from typing import List, Set


@dataclass
class Entry:
    signals: List[Set[str]]
    outputs: List[Set[str]]


def solve(input: List[str]) -> int:
    def parse_entry(input: str) -> Entry:
        signals, outputs = input.split(" | ")
        return Entry(
            [set(s) for s in signals.split()], [set(o) for o in outputs.split()]
        )

    entries = [parse_entry(line) for line in input]

    return sum(
        itertools.chain.from_iterable(
            map(lambda __: 1, filter(lambda d: len(d) in (2, 3, 4, 7), entry.outputs))
            for entry in entries
        )
    )


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
