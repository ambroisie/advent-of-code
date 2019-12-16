#!/usr/bin/env python

import sys
from functools import reduce
from itertools import chain, cycle
from typing import Iterable, List


def main() -> None:
    rep = 10000
    signal = [int(d) for d in sys.stdin.read().strip()] * rep
    offset = reduce(lambda a, b: a * 10 + b, signal[0:7])

    assert offset >= len(signal) / 2  # Sanity check
    # The trick is that the second half is only affected by itself (triangular matrix):
    # For i > len(signal) / 2, new_signal[i] = sum(signal, i, len(signal))
    # Therefore, we're only interested in numbers that start at the offset
    signal = signal[offset:]  # Only take the end we need

    for __ in range(100):
        for i in range(len(signal) - 1, 0, -1):  # Do the sum from the end
            signal[i - 1] += signal[i]
            signal[i - 1] = signal[i - 1] % 10

    print(reduce(lambda a, b: a * 10 + b, signal[:8]))


if __name__ == "__main__":
    main()
