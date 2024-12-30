#!/usr/bin/env python

import collections
import sys


def solve(input: str) -> int:
    def parse(input: str) -> tuple[int, int]:
        split = input.split()
        return int(split[0]), int(split[6])

    def play_game(players: int, last_marble: int) -> list[int]:
        circle = collections.deque([0])
        scores = [0] * players

        for marble in range(1, last_marble + 1):
            if marble % 23 == 0:
                scores[marble % players] += marble
                circle.rotate(7)
                scores[marble % players] += circle.pop()
                circle.rotate(-1)
            else:
                circle.rotate(-1)
                circle.append(marble)

        return scores

    players, last_marble = parse(input)
    scores = play_game(players, last_marble)
    return max(scores)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
