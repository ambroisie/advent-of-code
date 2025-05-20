#!/usr/bin/env python

import hashlib
import itertools
import sys


def solve(input: str) -> int:
    key = input.strip()
    for i in itertools.count(1):
        hash = hashlib.md5((key + str(i)).encode()).hexdigest()
        if hash.startswith("000000"):
            return i
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
