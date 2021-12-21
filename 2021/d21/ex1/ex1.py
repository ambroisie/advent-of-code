#!/usr/bin/env python

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


class GameState(NamedTuple):
    p1: PlayerStats
    p2: PlayerStats
    total_rolls: int


WINNING_SCORE = 1000


def solve(input: List[str]) -> int:
    def parse() -> Tuple[int, int]:
        p1, p2 = input[0].split(" ")[-1], input[1].split(" ")[-1]
        return int(p1), int(p2)

    def deterministic_die() -> Iterator[int]:
        return itertools.cycle(range(1, 100 + 1))

    def do_turn(stats: PlayerStats, rolls: Iterator[int]) -> PlayerStats:
        position, score = stats
        roll = sum(take(3, rolls))
        position = ((position - 1 + roll) % 10) + 1
        score += position
        return PlayerStats(position, score)

    def play_to_end(intial_state: GameState) -> GameState:
        p1, p2, total_rolls = intial_state
        die_rolls = deterministic_die()

        while True:
            p1 = do_turn(p1, die_rolls)
            total_rolls += 3
            if p1.score >= WINNING_SCORE:
                break
            p2 = do_turn(p2, die_rolls)
            total_rolls += 3
            if p2.score >= WINNING_SCORE:
                break

        return GameState(p1, p2, total_rolls)

    position1, position2 = parse()
    p1, p2, total_rolls = play_to_end(
        GameState(PlayerStats(position1, 0), PlayerStats(position2, 0), 0)
    )
    # The loser *must* have the lowest score
    return min(p1.score, p2.score) * total_rolls


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
