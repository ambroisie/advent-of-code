#!/usr/bin/env python

import sys
from dataclasses import dataclass
from math import ceil
from typing import Dict, List


@dataclass
class Ingredient:
    name: str
    quantity: int


@dataclass
class ReactionEquation:
    quantity: int
    inputs: List[Ingredient]


Reactions = Dict[str, ReactionEquation]


def solve_for(n: int, reactions: Reactions) -> int:
    ore_needed = 0
    wanted = [("FUEL", n)]
    excess: Dict[str, int] = {}

    def provide_ingredient(name: str, wanted_quantity: int) -> None:
        nonlocal ore_needed
        nonlocal excess
        nonlocal wanted

        if name == "ORE":
            ore_needed += wanted_quantity  # There's no recipy for this one
            return

        if name in excess:
            # Take from excess
            if excess[name] > wanted_quantity:
                excess[name] -= wanted_quantity
                return  # Nothing left to do
            wanted_quantity -= excess[name]
            del excess[name]  # Took everything

        if wanted_quantity == 0:  # In case we provided just enough by excess
            return

        equation = reactions[name]
        reaction_num = ceil(wanted_quantity / equation.quantity)

        for ingredient in equation.inputs:
            needed_quantity = ingredient.quantity * reaction_num
            provide_ingredient(ingredient.name, needed_quantity)

        produced_quantity = equation.quantity * reaction_num
        excess_quantity = produced_quantity - wanted_quantity
        if excess_quantity > 0:
            if name in excess:
                excess[name] += excess_quantity
            else:
                excess[name] = excess_quantity

    while len(wanted) != 0:
        provide_ingredient(*(wanted.pop()))

    return ore_needed


def main() -> None:
    reactions: Reactions = {}

    def parse_react(l: str) -> None:
        def parse_ingredient(i: str) -> Ingredient:
            quantity, name = i.strip().split(" ")
            return Ingredient(name, int(quantity))

        input_list, output_str = l.split("=>")
        inputs = [i for i in map(parse_ingredient, input_list.split(", "))]
        output = parse_ingredient(output_str)
        reactions[output.name] = ReactionEquation(output.quantity, inputs)

    for line in sys.stdin.readlines():
        parse_react(line)

    for_one = solve_for(1, reactions)
    target = 1000000000000
    # Educated guesses about minimum and maximum fuel needed to use 'target' ORE
    min_fuel_needed = target // for_one
    max_fuel_needed = 2 * min_fuel_needed
    while min_fuel_needed < max_fuel_needed:
        # We already know that minimum value is valid, offset it by one for the search
        mid = ceil((min_fuel_needed + max_fuel_needed) / 2)
        mid_res = solve_for(mid, reactions)
        if mid_res > target:
            # Exclude the maximum that was already searched
            max_fuel_needed = mid - 1
        else:
            # Keep the valid minimum value
            min_fuel_needed = mid

    print(max_fuel_needed)


if __name__ == "__main__":
    main()
