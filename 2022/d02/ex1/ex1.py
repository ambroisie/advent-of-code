#!/usr/bin/env python

import enum
import sys


class Outcome(enum.IntEnum):
    Lose = 0
    Draw = 3
    Win = 6


class Choice(enum.IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

    @classmethod
    def from_input(cls, input: str) -> "Choice":
        match input:
            case "A" | "X":
                return cls.Rock
            case "B" | "Y":
                return cls.Paper
            case "C" | "Z":
                return cls.Scissors
        assert False  # Sanity check


def score(other: Choice, you: Choice) -> int:
    def outcome() -> Outcome:
        if other == you:
            return Outcome.Draw
        if other == other.Rock and you == other.Paper:
            return Outcome.Win
        if other == other.Paper and you == other.Scissors:
            return Outcome.Win
        if other == other.Scissors and you == other.Rock:
            return Outcome.Win
        return Outcome.Lose

    return you + outcome()


Round = tuple[Choice, Choice]


def solve(input: list[Round]) -> int:
    return sum(map(lambda round: score(*round), input))


def main() -> None:
    input: list[Round] = [
        (Choice.from_input(round[0]), Choice.from_input(round[2]))
        for round in sys.stdin.readlines()
    ]
    print(solve(input))


if __name__ == "__main__":
    main()
