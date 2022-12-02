#!/usr/bin/env python

import enum
import sys


class Outcome(enum.IntEnum):
    Lose = 0
    Draw = 3
    Win = 6

    @classmethod
    def from_input(cls, input: str) -> "Outcome":
        match input:
            case "X":
                return cls.Lose
            case "Y":
                return cls.Draw
            case "Z":
                return cls.Win
        assert False  # Sanity check


class Choice(enum.IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

    @classmethod
    def from_input(cls, input: str) -> "Choice":
        match input:
            case "A":
                return cls.Rock
            case "B":
                return cls.Paper
            case "C":
                return cls.Scissors
        assert False  # Sanity check


def score(other: Choice, outcome: Outcome) -> int:
    def choice() -> Choice:
        match outcome:
            case Outcome.Lose:
                delta = -1
            case Outcome.Draw:
                delta = 0
            case Outcome.Win:
                delta = 1
        return Choice((other + delta - 1) % 3 + 1)

    return outcome + choice()


Round = tuple[Choice, Outcome]


def solve(input: list[Round]) -> int:
    return sum(map(lambda round: score(*round), input))


def main() -> None:
    input: list[Round] = [
        (Choice.from_input(round[0]), Outcome.from_input(round[2]))
        for round in sys.stdin.readlines()
    ]
    print(solve(input))


if __name__ == "__main__":
    main()
