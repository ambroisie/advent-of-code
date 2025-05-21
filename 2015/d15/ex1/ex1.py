#!/usr/bin/env python

import sys
from collections.abc import Iterator
from typing import NamedTuple


class Properties(NamedTuple):
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @classmethod
    def from_str(cls, input: str) -> "Properties":
        properties = map(str.split, input.split(", "))
        return cls(*(int(prop[-1]) for prop in properties))


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[str, Properties]:
        ingredient, properties = input.split(": ")
        return ingredient, Properties.from_str(properties)

    def parse(input: str) -> dict[str, Properties]:
        return {name: prop for name, prop in map(parse_line, input.splitlines())}

    def score(ingredients: dict[str, Properties], amounts: dict[str, int]) -> int:
        assert ingredients.keys() == amounts.keys()  # Sanity check
        assert sum(amounts.values()) == 100  # Sanity check
        res = 1
        for prop in ("capacity", "durability", "flavor", "texture"):
            res *= max(
                0,
                sum(
                    getattr(ingredients[name], prop) * amounts[name]
                    for name in ingredients.keys()
                ),
            )
        return res

    def permute_amounts(ingredients: dict[str, Properties]) -> Iterator[dict[str, int]]:
        def helper(amounts: dict[str, int]) -> Iterator[dict[str, int]]:
            remaining = 100 - sum(amounts.values())
            assert remaining >= 0  # Sanity check
            assert ingredients  # Sanity check

            current = next(iter(n for n in ingredients.keys() if n not in amounts))
            if (len(amounts) + 1) == len(ingredients):
                yield amounts | {current: remaining}
            else:
                for i in range(remaining):
                    yield from helper(amounts | {current: i})

        yield from helper({})

    def maximize_score(ingredient: dict[str, Properties]) -> int:
        return max(
            score(ingredient, amounts) for amounts in permute_amounts(ingredients)
        )

    ingredients = parse(input)
    return maximize_score(ingredients)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
