#!/usr/bin/env python

import sys
from collections import Counter
from enum import StrEnum


class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


Round = Counter[Color]
Game = list[Round]

# The input is in order without skipping, but just in case...
GameRecord = dict[int, Game]

BAG_CONTENTS = Counter(
    {
        Color.RED: 12,
        Color.GREEN: 13,
        Color.BLUE: 14,
    }
)


def solve(input: list[str]) -> int:
    def parse_round(round: str) -> Round:
        values = (value.split(" ") for value in round.split(", "))
        return Counter({Color(c): int(n) for n, c in values})

    # This does *not* expect the "Game <int>:" bit
    def parse_game(game: str) -> Game:
        rounds = game.split("; ")
        return [parse_round(r) for r in rounds]

    def parse_line(line: str) -> tuple[int, Game]:
        game_id, rounds = line.split(": ")
        return int(game_id.removeprefix("Game ")), parse_game(rounds)

    def parse(input: list[str]) -> GameRecord:
        parsed = map(parse_line, input)
        return {id: game for id, game in parsed}

    def game_is_valid(game: Game) -> bool:
        for round in game:
            for c in Color:
                if round[c] > BAG_CONTENTS[c]:
                    return False

        return True

    games = parse(input)
    return sum(id for id, game in games.items() if game_is_valid(game))


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
