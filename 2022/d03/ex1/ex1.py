#!/usr/bin/env python

import sys


def solve(input: list[str]) -> int:
    def score(line: str) -> int:
        common_items = set(line[: len(line) // 2]) & set(line[len(line) // 2 :])
        assert len(common_items) == 1  # Sanity check
        common = common_items.pop()
        return common.isupper() * 26 + ord(common.lower()) - ord("a") + 1

    return sum(map(lambda line: score(line), input))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
