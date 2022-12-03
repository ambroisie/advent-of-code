#!/usr/bin/env python

import sys
from collections.abc import Iterator

Group = tuple[str, str, str]


def solve(input: list[str]) -> int:
    def score(lines: Group) -> int:
        common_items = set(lines[0]) & set(lines[1]) & set(lines[2])
        assert len(common_items) == 1  # Sanity check
        common = common_items.pop()
        return common.isupper() * 26 + ord(common.lower()) - ord("a") + 1

    def iter_3() -> Iterator[Group]:
        args = [iter(input)] * 3
        yield from zip(*args, strict=True)  # type: ignore

    return sum(map(score, iter_3()))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
