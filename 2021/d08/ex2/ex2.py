#!/usr/bin/env python

import itertools
import sys
from dataclasses import dataclass
from typing import Dict, List, Set


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

    def deduce_signals(entry: Entry) -> Dict[int, Set[str]]:
        _1, _7, _4, *signals_to_deduce, _8 = sorted(entry.signals, key=len)
        signals = {
            1: _1,
            4: _4,
            7: _7,
            8: _8,
        }

        for sig in signals_to_deduce:
            match = len(sig), len(sig & _4), len(sig & _1)

            if match == (6, 3, 2):
                signals[0] = sig
            elif match == (5, 2, 1):
                signals[2] = sig
            elif match == (5, 3, 2):
                signals[3] = sig
            elif match == (5, 3, 1):
                signals[5] = sig
            elif match == (6, 3, 1):
                signals[6] = sig
            elif match == (6, 4, 2):
                signals[9] = sig
            else:
                assert False  # Sanity check

        assert len(signals) == 10  # Sanity check
        return signals

    def deduce_entry(entry: Entry) -> int:
        decoded_signals = deduce_signals(entry)

        res = 0

        for output in entry.outputs:
            assert output in decoded_signals.values()  # Sanity check

            for n, signal in decoded_signals.items():
                if output != signal:
                    continue
                res = res * 10 + n

        return res

    entries = [parse_entry(line) for line in input]

    return sum(map(deduce_entry, entries))


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
