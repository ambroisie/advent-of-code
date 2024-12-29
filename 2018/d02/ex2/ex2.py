#!/usr/bin/env python

import itertools
import sys


def solve(input: str) -> str:
    def find_box_ids(boxes: list[str]) -> str:
        for lhs, rhs in itertools.combinations(boxes, 2):
            assert len(lhs) == len(rhs)  # Sanity check
            for i in range(len(lhs)):
                if lhs[:i] == rhs[:i] and lhs[i + 1 :] == rhs[i + 1 :]:
                    return lhs[:i] + lhs[i + 1 :]
        assert False  # Sanity check

    boxes = input.splitlines()
    return find_box_ids(boxes)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
