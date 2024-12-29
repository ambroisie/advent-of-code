#!/usr/bin/env python

import sys
from collections import Counter


def solve(input: str) -> int:
    def any_letter(boxes: list[str], count: int) -> int:
        return sum(count in Counter(box).values() for box in boxes)

    def checksum(boxes: list[str]) -> int:
        return any_letter(boxes, 2) * any_letter(boxes, 3)

    boxes = input.splitlines()
    return checksum(boxes)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
