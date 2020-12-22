#!/usr/bin/env python

import itertools
import sys
from collections import deque
from typing import Deque, List, Tuple

Deck = Deque[int]


def parse_decks(raw: List[str]) -> Tuple[Deck, Deck]:
    deck_1 = deque(int(n) for n in itertools.takewhile(len, raw[1:]))
    deck_2 = deque(
        int(n) for n in itertools.islice(itertools.dropwhile(len, raw[1:]), 2, None)
    )
    return deck_1, deck_2


def play(deck_1: Deck, deck_2: Deck) -> Tuple[int, Deck]:
    while len(deck_1) and len(deck_2):
        left, right = deck_1.popleft(), deck_2.popleft()
        if left > right:
            deck_1.extend((left, right))
        else:
            deck_2.extend((right, left))
    return (1, deck_1) if len(deck_1) else (2, deck_2)


def solve(raw: List[str]) -> int:
    __, deck = play(*parse_decks(raw))

    score = sum((i) * val for i, val in enumerate(reversed(deck), 1))

    return score


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
