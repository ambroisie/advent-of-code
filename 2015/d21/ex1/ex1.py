#!/usr/bin/env python

import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Ennemy(NamedTuple):
    hp: int
    damage: int
    armor: int

    def attack(self, other: "Ennemy") -> "Ennemy":
        return Ennemy(
            other.hp - max(1, self.damage - other.armor),
            other.damage,
            other.armor,
        )


class Item(NamedTuple):
    cost: int
    damage: int
    armor: int


WEAPONS = {
    "Dagger": Item(8, 4, 0),
    "Shortsword": Item(10, 5, 0),
    "Warhammer": Item(25, 6, 0),
    "Longsword": Item(40, 7, 0),
    "Greataxe": Item(74, 8, 0),
}
ARMORS = {
    "Leather": Item(13, 0, 1),
    "Chainmail": Item(31, 0, 2),
    "Splintmail": Item(53, 0, 3),
    "Bandedmail": Item(75, 0, 4),
    "Platemail": Item(102, 0, 5),
}
RINGS = {
    "Damage +1": Item(25, 1, 0),
    "Damage +2": Item(50, 2, 0),
    "Damage +3": Item(100, 3, 0),
    "Defense +1": Item(20, 0, 1),
    "Defense +2": Item(40, 0, 2),
    "Defense +3": Item(80, 0, 3),
}


def solve(input: str) -> int:
    def parse(input: str) -> Ennemy:
        return Ennemy(*map(int, (line.split(": ")[1] for line in input.splitlines())))

    def choose_items() -> Iterator[list[Item]]:
        allowed_weapons = [1]
        allowed_armors = [0, 1]
        allowed_rings = [0, 1, 2]

        for weapons, armors, rings in itertools.product(
            itertools.chain.from_iterable(
                itertools.combinations(WEAPONS.values(), i) for i in allowed_weapons
            ),
            itertools.chain.from_iterable(
                itertools.combinations(ARMORS.values(), i) for i in allowed_armors
            ),
            itertools.chain.from_iterable(
                itertools.combinations(RINGS.values(), i) for i in allowed_rings
            ),
        ):
            yield list(itertools.chain(weapons, armors, rings))

    def assemble_inventory(items: list[Item]) -> Ennemy:
        return Ennemy(
            hp=100,
            damage=sum(item.damage for item in items),
            armor=sum(item.armor for item in items),
        )

    def battle(us: Ennemy, ennemy: Ennemy) -> bool:
        while True:
            ennemy = us.attack(ennemy)
            if ennemy.hp <= 0:
                return True
            us = ennemy.attack(us)
            if us.hp <= 0:
                return False

    ennemy = parse(input)
    return min(
        sum(item.cost for item in items)
        for items in choose_items()
        if battle(assemble_inventory(items), ennemy)
    )


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
