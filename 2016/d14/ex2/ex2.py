#!/usr/bin/env python

import functools
import hashlib
import itertools
import sys


def solve(input: str) -> int:
    def hash(n: int, salt: str) -> str:
        key = salt + str(n)
        for _ in range(2016 + 1):
            key = hashlib.md5(key.encode()).hexdigest()
        return key

    def find_triplet_char(input: str) -> str | None:
        for i in range(0, len(input) - 2):
            a, b, c = input[i], input[i + 1], input[i + 2]
            if a == b and b == c:
                return a
        return None

    salt = input.strip()
    hashed_salt = functools.cache(functools.partial(hash, salt=salt))
    cur_key = 0
    for i in itertools.count():
        candidate = hashed_salt(i)
        if (triplet_char := find_triplet_char(candidate)) is None:
            continue
        for j in range(i + 1, i + 1000 + 1):
            if (triplet_char * 5) in hashed_salt(j):
                cur_key += 1
                if cur_key == 64:
                    return i
                break
    assert False  # Sanity check


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
