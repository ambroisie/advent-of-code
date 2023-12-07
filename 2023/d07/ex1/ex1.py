#!/usr/bin/env python

import functools
import sys
from collections import Counter

Play = tuple[str, int]

ORDER = "23456789TJQKA"


def solve(input: list[str]) -> int:
    def parse(input: list[str]) -> list[Play]:
        return [(hand, int(bid)) for hand, bid in map(str.split, input)]

    # Stronger hands compare higher than weaker hands
    def cmp_hand(lhs: str, rhs: str) -> int:
        def to_type(hand: str) -> list[int]:
            return [count for _, count in Counter(hand).most_common()]

        def cmp_type(lhs: list[int], rhs: list[int]) -> int:
            for left, right in zip(lhs, rhs):
                if (cmp := left - right) != 0:
                    return cmp
            return 0

        def cmp_card(lhs: str, rhs: str) -> int:
            assert lhs in ORDER and rhs in ORDER  # Sanity check
            assert len(lhs) == 1 and len(rhs) == 1  # Sanity check
            return ORDER.find(lhs) - ORDER.find(rhs)

        if (cmp := cmp_type(to_type(lhs), to_type(rhs))) != 0:
            return cmp

        for left, right in zip(lhs, rhs):
            if (cmp := cmp_card(left, right)) != 0:
                return cmp

        return 0

    def cmp_play(lhs: Play, rhs: Play) -> int:
        return cmp_hand(lhs[0], rhs[0])

    plays = parse(input)
    plays = sorted(plays, key=functools.cmp_to_key(cmp_play))

    return sum(rank * bid for rank, (_, bid) in enumerate(plays, start=1))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
