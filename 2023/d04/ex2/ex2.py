#!/usr/bin/env python

import dataclasses
import sys


@dataclasses.dataclass
class Card:
    win_nums: set[int]
    nums: set[int]
    copies: int = 1


# The input is in order without skipping, but just in case...
Cards = dict[int, Card]


def solve(input: list[str]) -> int:
    def parse_nums(nums: str) -> set[int]:
        return {int(n) for n in nums.split(" ") if n != ""}

    # This does *not* expect the "Card <int>:" bit
    def parse_card(card: str) -> Card:
        win_nums, nums = card.split("|")
        return Card(
            win_nums=parse_nums(win_nums),
            nums=parse_nums(nums),
        )

    def parse_line(line: str) -> tuple[int, Card]:
        card_id, card = line.split(": ")
        return int(card_id.removeprefix("Card")), parse_card(card)

    def parse(input: list[str]) -> Cards:
        parsed = map(parse_line, input)
        return {id: card for id, card in parsed}

    def score(card: Card) -> int:
        actual_win_nums = card.nums & card.win_nums
        return len(actual_win_nums)

    cards = parse(input)
    for i, card in cards.items():
        winnings = score(card)
        for n in range(1, winnings + 1):
            cards[i + n].copies += card.copies

    return sum(card.copies for card in cards.values())


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
