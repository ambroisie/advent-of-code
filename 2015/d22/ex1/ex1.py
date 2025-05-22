#!/usr/bin/env python

import heapq
import sys
from collections.abc import Iterator
from typing import NamedTuple


class Ennemy(NamedTuple):
    hp: int
    damage: int


class Effects(NamedTuple):
    # Effect is active is it is greater or equal to zero
    shield: int = -1
    poison: int = -1
    recharge: int = -1

    def tick(self) -> "Effects":
        return Effects(*(n - 1 for n in self))

    def shield_active(self) -> bool:
        return self.shield >= 0

    def poison_active(self) -> bool:
        return self.poison >= 0

    def recharge_active(self) -> bool:
        return self.recharge >= 0

    def with_shield(self) -> "Effects":
        assert self.shield <= 0  # Sanity check
        return self._replace(shield=6)

    def with_poison(self) -> "Effects":
        assert self.poison <= 0  # Sanity check
        return self._replace(poison=6)

    def with_recharge(self) -> "Effects":
        assert self.recharge <= 0  # Sanity check
        return self._replace(recharge=5)


class Player(NamedTuple):
    hp: int
    mana: int
    effects: Effects


MISSILE = 53
DRAIN = 73
SHIELD = 113
POISON = 173
RECHARGE = 229


def solve(input: str) -> int:
    def parse(input: str) -> Ennemy:
        return Ennemy(*map(int, (line.split(": ")[1] for line in input.splitlines())))

    def step(player: Player, ennemy: Ennemy) -> Iterator[tuple[int, Player, Ennemy]]:
        def tick_spells(player: Player, ennemy: Ennemy) -> tuple[Player, Ennemy]:
            player = player._replace(effects=player.effects.tick())
            if player.effects.recharge_active():
                player = player._replace(mana=player.mana + 101)
            if player.effects.poison_active():
                ennemy = ennemy._replace(hp=ennemy.hp - 3)
            return player, ennemy

        # Note: does *not* drain the mana for the spell
        def possible_spells(
            player: Player,
            ennemy: Ennemy,
        ) -> Iterator[tuple[int, Player, Ennemy]]:
            if player.mana >= MISSILE:
                yield (
                    MISSILE,
                    player,
                    ennemy._replace(hp=ennemy.hp - 4),
                )
            if player.mana >= DRAIN:
                yield (
                    DRAIN,
                    player._replace(hp=player.hp + 2),
                    ennemy._replace(hp=ennemy.hp - 2),
                )
            if player.mana >= SHIELD and player.effects.shield <= 0:
                yield (
                    SHIELD,
                    player._replace(effects=player.effects.with_shield()),
                    ennemy,
                )
            if player.mana >= POISON and player.effects.poison <= 0:
                yield (
                    POISON,
                    player._replace(effects=player.effects.with_poison()),
                    ennemy,
                )
            if player.mana >= RECHARGE and player.effects.recharge <= 0:
                yield (
                    RECHARGE,
                    player._replace(effects=player.effects.with_recharge()),
                    ennemy,
                )

        def boss_turn(player: Player, ennemy: Ennemy) -> tuple[Player, Ennemy]:
            # Spells are ticked at start of turn
            player, ennemy = tick_spells(player, ennemy)

            # Ennemy can't attack if they're dead
            if ennemy.hp <= 0:
                return player, ennemy

            armor = 7 if player.effects.shield_active() else 0
            damage = max(1, ennemy.damage - armor)
            return player._replace(hp=player.hp - damage), ennemy

        # We lose if we run out of hp
        if player.hp <= 0:
            return

        # Spells are ticked at start of turn
        player, ennemy = tick_spells(player, ennemy)

        # Don't spend a spell if the ennemy is already dead
        if ennemy.hp <= 0:
            yield 0, player, ennemy

        for cost, player, ennemy in possible_spells(player, ennemy):
            yield cost, *boss_turn(player._replace(mana=player.mana - cost), ennemy)

    def dijkstra(player: Player, ennemy: Ennemy) -> int:
        # Priority queue of (mana_spent, player, ennemy)
        queue = [(0, player, ennemy)]
        seen: set[tuple[Player, Ennemy]] = set()

        while len(queue) > 0:
            total_cost, p, e = heapq.heappop(queue)
            if p.hp <= 0:
                continue
            if e.hp <= 0:
                return total_cost
            # We must have seen (p, e) with a smaller distance before
            if (p, e) in seen:
                continue
            # First time encountering (p, e), must be the smallest distance to it
            seen.add((p, e))
            # Add all neighbours to be visited
            for cost, p, e in step(p, e):
                heapq.heappush(queue, (total_cost + cost, p, e))

        assert False  # Sanity check

    ennemy = parse(input)
    player = Player(50, 500, Effects())
    return dijkstra(player, ennemy)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
