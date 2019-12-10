#!/usr/bin/env python

import sys


def main() -> None:
    COLUMNS = 25
    ROWS = 6
    digits = [int(d) for d in str(int(sys.stdin.read()))]

    assert len(digits) % (COLUMNS * ROWS) == 0  # Sanity check
    LAYERS = int(len(digits) / (COLUMNS * ROWS))

    layers = [
        [digits.pop(0) for __ in range(COLUMNS) for __ in range(ROWS)]
        for __ in range(LAYERS)
    ]

    least_zeros = min(layers, key=lambda l: sum(1 for d in l if d == 0))

    print(sum(1 for d in least_zeros if d == 1) * sum(1 for d in least_zeros if d == 2))


if __name__ == "__main__":
    main()
