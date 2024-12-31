#!/usr/bin/env python

import copy
import dataclasses
import enum
import sys


@dataclasses.dataclass
class Group:
    units: int
    hp: int
    weaknesses: set[str]
    immunities: set[str]
    attack: int
    attack_type: str
    initiative: int

    @classmethod
    def from_raw(cls, input: str) -> "Group":
        def split_sections(input: str) -> tuple[str, str, str]:
            points_idx = input.index("hit points ")
            with_idx = input.index(" with an attack")
            return (
                input[:points_idx].strip(),
                input[points_idx:with_idx].removeprefix("(").removesuffix(")"),
                input[with_idx:].strip(),
            )

        def parse_weak_immune(weak_immune: str) -> tuple[set[str], set[str]]:
            weaknesses: set[str] = set()
            immunities: set[str] = set()
            for part in weak_immune.split("; "):
                for start, values in (
                    ("weak to ", weaknesses),
                    ("immune to ", immunities),
                ):
                    if not part.startswith(start):
                        continue
                    values.update(part.removeprefix(start).split(", "))
            return weaknesses, immunities

        group_str, weak_immune, attack_str = split_sections(input)
        group_list, attack_list = group_str.split(), attack_str.split()
        weaknesses, immunities = parse_weak_immune(
            weak_immune.removeprefix("hit points (")
        )
        return cls(
            units=int(group_list[0]),
            hp=int(group_list[4]),
            weaknesses=weaknesses,
            immunities=immunities,
            attack=int(attack_list[5]),
            attack_type=attack_list[6],
            initiative=int(attack_list[10]),
        )

    @property
    def alive(self) -> bool:
        return self.units > 0

    @property
    def effective_power(self) -> int:
        return self.units * self.attack

    def potential_attack(self, ennemy: "Group") -> int:
        multiplier = 1
        if self.attack_type in ennemy.weaknesses:
            multiplier = 2
        if self.attack_type in ennemy.immunities:
            multiplier = 0
        return self.effective_power * multiplier


class LoopError(Exception):
    pass


class Army(enum.StrEnum):
    INFECTION = "INFECTION"
    IMMUNE = "IMMUNE"

    def ennemy(self) -> "Army":
        if self == Army.INFECTION:
            return Army.IMMUNE
        if self == Army.IMMUNE:
            return Army.INFECTION
        assert False  # Sanity check


@dataclasses.dataclass
class Armies:
    immune: list[Group]
    infection: list[Group]

    @classmethod
    def from_raw(cls, input: str) -> "Armies":
        immune, infection = map(str.splitlines, input.split("\n\n"))
        assert "Immune System:" == immune[0]  # Sanity check
        assert "Infection:" == infection[0]  # Sanity check
        return cls(
            list(map(Group.from_raw, immune[1:])),
            list(map(Group.from_raw, infection[1:])),
        )

    def army(self, army: Army) -> list[Group]:
        if army == Army.IMMUNE:
            return self.immune
        if army == Army.INFECTION:
            return self.infection
        assert False  # Sanity check

    def active_groups(self, army: Army) -> set[int]:
        return {i for i, group in enumerate(self.army(army)) if group.alive}

    def selection_phase(self) -> dict[tuple[Army, int], int]:
        # Armies are sorted by decreasing power, initiative
        def power_order(group: Group) -> tuple[int, int]:
            return group.effective_power, group.initiative

        # Targets are ordered in decreasing potential attack, power, initiative
        def target_order(group: Group, ennemy: Group) -> tuple[int, int, int]:
            return (
                group.potential_attack(ennemy),
                ennemy.effective_power,
                ennemy.initiative,
            )

        res: dict[tuple[Army, int], int] = {}
        for army in Army:
            army_indices = sorted(
                self.active_groups(army),
                key=lambda i: power_order(self.army(army)[i]),
                reverse=True,
            )
            ennemies = self.army(army.ennemy())
            indices = set(self.active_groups(army.ennemy()))
            for i in army_indices:
                group = self.army(army)[i]
                if not indices:
                    break
                target = max(indices, key=lambda j: target_order(group, ennemies[j]))
                # Skip target if we cannot deal damage to it
                if group.potential_attack(ennemies[target]) == 0:
                    continue
                res[(army, i)] = target
                # Targets must be different for each attack
                indices.remove(target)
        return res

    def attack_phase(self, targets: dict[tuple[Army, int], int]) -> None:
        # Armies take turn by initiative, regardless of type
        turn_order = sorted(
            ((army, i) for army in Army for i in self.active_groups(army)),
            key=lambda t: self.army(t[0])[t[1]].initiative,
            reverse=True,
        )
        any_kills = False
        for army, i in turn_order:
            # Empty armies do not fight
            if not self.army(army)[i].alive:
                continue
            # Army must have a target selected
            if (target := targets.get((army, i))) is None:
                continue
            attackers = self.army(army)[i]
            defender = self.army(army.ennemy())[target]
            damage = attackers.potential_attack(defender)
            killed_units = min(damage // defender.hp, defender.units)
            defender.units -= killed_units
            # Detect if no kills were done to avoid loops
            any_kills |= bool(killed_units)
        # If no units were killed, we're about to enter an infinite loop
        if not any_kills:
            raise LoopError

    def fight(self) -> None:
        while self.active_groups(Army.IMMUNE) and self.active_groups(Army.INFECTION):
            targets = self.selection_phase()
            self.attack_phase(targets)


def solve(input: str) -> int:
    def parse(input: str) -> Armies:
        return Armies.from_raw(input)

    def apply_boost(armies: Armies, boost: int) -> int:
        armies = copy.deepcopy(armies)
        for group in armies.immune:
            group.attack += boost
        try:
            armies.fight()
        except LoopError:
            return 0
        return sum(group.units for group in armies.immune)

    def bisect_boost(armies: Armies) -> int:
        # Winning the fight feels like it should be monotonic
        low, high = 0, 100000  # Probably good enough
        while low < high:
            mid = low + (high - low) // 2
            if apply_boost(armies, mid) != 0:
                high = mid
            else:
                low = mid + 1
        # Wastefully re-run the fight to get the number of remaining units
        return apply_boost(armies, low)

    armies = parse(input)
    return bisect_boost(armies)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
