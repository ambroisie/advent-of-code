#!/usr/bin/env python

import functools
import re
import sys
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List, Set, Tuple


def parse(raw: List[str]) -> Tuple[List[Set[str]], List[Set[str]]]:
    def parse_ingredients(line: str) -> Set[str]:
        pos = line.find(" (contains ")
        if pos != -1:
            line = line[:pos]
        return set(line.split())

    def parse_allergens(line: str) -> Set[str]:
        pos = line.find("(contains ")
        if pos == -1:
            return set()
        return set(re.findall("([^ ]+)[,\\)]", line))

    ingredients = []
    allergens = []

    for line in raw:
        ingredients.append(parse_ingredients(line))
        allergens.append(parse_allergens(line))

    return ingredients, allergens


def find_allergens(
    ingredients: List[Set[str]], allergens: List[Set[str]]
) -> Dict[str, Set[str]]:
    all_ingredients = functools.reduce(lambda lhs, rhs: lhs | rhs, ingredients)
    possibilities: Dict[str, Set[str]] = defaultdict(lambda: deepcopy(all_ingredients))

    for ing, all in zip(ingredients, allergens):
        for allergen in all:
            possibilities[allergen] &= set(ing)

    return dict(possibilities)


def cross_eliminate(possibilities: Dict[str, Set[str]]) -> None:
    while True:
        eliminated = False
        for pos in possibilities:
            if len(possibilities[pos]) != 1:
                continue
            for other_pos in possibilities:
                if other_pos == pos:
                    continue
                if len(possibilities[other_pos] & possibilities[pos]) == 0:
                    continue
                eliminated = True
                possibilities[other_pos] -= possibilities[pos]
        if not eliminated:
            break


def solve(raw: List[str]) -> str:
    ingredients, allergens = parse(raw)
    possibilities = find_allergens(ingredients, allergens)
    cross_eliminate(possibilities)
    matches = [
        (ingredient.pop(), allergen) for allergen, ingredient in possibilities.items()
    ]
    matches.sort(key=lambda tup: tup[1])
    return ",".join(ingredient for ingredient, __ in matches)


def main() -> None:
    input = [line.strip() for line in sys.stdin]
    print(solve(input))


if __name__ == "__main__":
    main()
