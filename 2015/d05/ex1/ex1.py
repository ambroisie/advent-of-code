#!/usr/bin/env python

import collections
import sys


def solve(input: str) -> int:
    def is_nice(input: str) -> bool:
        counts = collections.Counter(input)
        if sum(counts[c] for c in "aeiou") < 3:
            return False
        if not any((c + c) in input for c in (chr(ord("a") + i) for i in range(26))):
            return False
        for bad in ("ab", "cd", "pq", "xy"):
            if bad in input:
                return False
        return True

    return sum(map(is_nice, input.splitlines()))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
