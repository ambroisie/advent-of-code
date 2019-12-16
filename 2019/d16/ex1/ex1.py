#!/usr/bin/env python

import sys
from functools import reduce
from itertools import chain, cycle
from typing import Iterable, List


def sequencer(pattern: List[int], n: int) -> Iterable[int]:
    gen = cycle(list(chain(*([a] * n for a in pattern))))
    next(gen)  # Skip the first one
    yield from gen


def main() -> None:
    signal = [int(d) for d in sys.stdin.read().strip()]
    base_pattern = [0, 1, 0, -1]

    for __ in range(100):
        signal = [
            abs(sum(a * b for a, b in zip(signal, sequencer(base_pattern, i + 1)))) % 10
            for i in range(len(signal))
        ]

    print(reduce(lambda a, b: a * 10 + b, signal[0:8]))


if __name__ == "__main__":
    main()
