#!/usr/bin/env python

import functools
import itertools
import sys
from typing import Iterable, Iterator, List, NamedTuple, Tuple, TypeVar

T = TypeVar("T")


def grouper(iterable: Iterable[T], n: int) -> Iterator[Tuple[T, ...]]:
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def take(n: int, iterable: Iterable[T]) -> List[T]:
    return list(itertools.islice(iterable, n))


class PlayerStats(NamedTuple):
    position: int
    score: int


ROLL_TO_UNIVERSES = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}

WINNING_SCORE = 21


def solve(input: List[str]) -> int:
    def parse() -> Tuple[int, int]:
        p1, p2 = input[0].split(" ")[-1], input[1].split(" ")[-1]
        return int(p1), int(p2)

    def do_turn(stats: PlayerStats, roll: int) -> PlayerStats:
        position, score = stats
        position = ((position - 1 + roll) % 10) + 1
        score += position
        return PlayerStats(position, score)

    @functools.cache
    def play_universes(p1: PlayerStats, p2: PlayerStats) -> Tuple[int, int]:
        p1_wins, p2_wins = 0, 0

        # Only 9 different outcomes from a 3d3 roll, with differing probabilities
        for roll, roll_probability in ROLL_TO_UNIVERSES.items():
            new_p1 = do_turn(p1, roll)
            if new_p1.score >= WINNING_SCORE:
                # Account for differing number of split universes when counting a win
                p1_wins += roll_probability
                continue

            # Exchange p1 and p2 roles, count their wins, and account for number of splits
            new_p2_wins, new_p1_wins = play_universes(p2, new_p1)
            p1_wins += new_p1_wins * roll_probability
            p2_wins += new_p2_wins * roll_probability

        return p1_wins, p2_wins

    p1, p2 = parse()
    p1_wins, p2_wins = play_universes(PlayerStats(p1, 0), PlayerStats(p2, 0))
    return max(p1_wins, p2_wins)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
