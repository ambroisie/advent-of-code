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

    ans = []
    for pixels in zip(*(layer for layer in layers)):
        ans.append(next(color for color in pixels if color != 2))

    print(
        "\n".join(
            "".join("█" if ans.pop(0) == 0 else " " for __ in range(COLUMNS))
            for __ in range(ROWS)
        )
    )


if __name__ == "__main__":
    main()
