#!/usr/bin/env python

import copy
import dataclasses
import enum
import itertools
import sys
from typing import Iterator, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    # Returned in reading order
    def neighbours(self) -> Iterator["Point"]:
        for dx, dy in (
            (-1, 0),
            (0, -1),
            (0, 1),
            (1, 0),
        ):
            yield Point(self.x + dx, self.y + dy)


class Unit(enum.StrEnum):
    ELF = "E"
    GOBLIN = "G"

    def ennemy(self) -> "Unit":
        if self == Unit.ELF:
            return Unit.GOBLIN
        if self == Unit.GOBLIN:
            return Unit.ELF
        assert False  # Sanity check


@dataclasses.dataclass
class UnitData:
    hp: int = 200
    power: int = 3


class ElfDiedError(Exception):
    pass


def solve(input: str) -> int:
    def parse(input: list[str]) -> tuple[set[Point], dict[Unit, set[Point]]]:
        walls: set[Point] = set()
        units: dict[Unit, set[Point]] = {u: set() for u in Unit}

        for x, line in enumerate(input):
            for y, c in enumerate(line):
                p = Point(x, y)
                if c in Unit:
                    units[Unit(c)].add(p)
                if c == "#":
                    walls.add(p)

        return walls, units

    def double_bfs(
        unit_type: Unit,
        unit_pos: Point,
        walls: set[Point],
        units: dict[Unit, set[Point]],
    ) -> Point | None:
        def bfs(
            start: Point,
            targets: set[Point],
            blockers: set[Point],
        ) -> Point | None:
            frontier = [start]
            seen: set[Point] = set()
            while frontier:
                new_frontier: set[Point] = set()

                for p in frontier:
                    if p in targets:
                        return p
                    seen.add(p)
                    for n in p.neighbours():
                        if n in seen:
                            continue
                        if n in blockers:
                            continue
                        new_frontier.add(n)
                frontier = sorted(new_frontier)

            return None

        blockers = walls | units[unit_type]
        ennemies = units[unit_type.ennemy()]

        # First BFS from start to square next to an ennemy
        targets_in_range = {
            n for ennemy in ennemies for n in ennemy.neighbours() if n not in blockers
        }
        if (target := bfs(unit_pos, targets_in_range, blockers)) is None:
            return None

        # Then back from chosen target to one of the movement squares
        movement_squares = {n for n in unit_pos.neighbours() if n not in blockers}
        return bfs(target, movement_squares, blockers)

    def do_move(
        unit_type: Unit,
        unit_pos: Point,
        walls: set[Point],
        units: dict[Unit, set[Point]],
        unit_data: dict[Point, UnitData],
    ) -> Point:
        # If already next to an ennemy, do not move
        if any(n in units[unit_type.ennemy()] for n in unit_pos.neighbours()):
            return unit_pos

        new_pos = double_bfs(unit_type, unit_pos, walls, units)

        # Nowhere to move to, no-op
        if new_pos is None:
            return unit_pos

        assert new_pos != unit_pos  # Sanity check
        assert unit_pos in units[unit_type]  # Sanity check
        assert new_pos not in units[unit_type]  # Sanity check

        # Make the movement in-place
        units[unit_type] ^= {unit_pos, new_pos}
        unit_data[new_pos] = unit_data.pop(unit_pos)

        return new_pos

    def do_attack(
        unit_type: Unit,
        unit_pos: Point,
        units: dict[Unit, set[Point]],
        unit_data: dict[Point, UnitData],
    ) -> None:
        # Look for an attack target
        target = min(
            (n for n in unit_pos.neighbours() if n in units[unit_type.ennemy()]),
            key=lambda p: unit_data[p].hp,
            default=None,
        )

        # If not in range, no-op
        if target is None:
            return

        assert target not in units[unit_type]  # Sanity check
        assert target in units[unit_type.ennemy()]  # Sanity check
        assert unit_data[target].hp > 0  # Sanity check

        # Make the attack in-place
        unit_data[target].hp -= unit_data[unit_pos].power
        # And if we killed it, remove it from `units`
        if unit_data[target].hp <= 0:
            if unit_type.ennemy() == Unit.ELF:
                raise ElfDiedError
            units[unit_type.ennemy()].remove(target)
            unit_data.pop(target)

    def turn(
        walls: set[Point],
        units: dict[Unit, set[Point]],
        unit_data: dict[Point, UnitData],
    ) -> bool:
        turn_order = sorted((p, u) for u, points in units.items() for p in points)
        for p, u in turn_order:
            # Don't do anything if the unit is dead
            if p not in units[u]:
                continue

            # If no ennemies left, finish the turn early and indicate that we're done
            if not units[u.ennemy()]:
                return False

            # Movements and attacks are made in-place
            p = do_move(u, p, walls, units, unit_data)
            do_attack(u, p, units, unit_data)

        return True

    def print_map(walls: set[Point], units: dict[Unit, set[Point]]) -> None:
        max_x, max_y = max(p.x for p in walls), max(p.y for p in walls)
        for x in range(0, max_x + 1):
            for y in range(0, max_y + 1):
                p = Point(x, y)
                for u in Unit:
                    if p in units[u]:
                        print(str(u), end="")
                        break
                else:
                    print("#" if p in walls else ".", end="")
            print()
        print()

    def run_to_completion(
        walls: set[Point],
        units: dict[Unit, set[Point]],
        unit_data: dict[Point, UnitData],
    ) -> int:
        turns = 0
        while turn(walls, units, unit_data):
            turns += 1
        return turns * sum(data.hp for data in unit_data.values())

    def arm_elves(
        walls: set[Point],
        units: dict[Unit, set[Point]],
    ) -> int:
        for elf_power in itertools.count(start=3):
            try:
                unit_data = {
                    p: UnitData(power=elf_power if u == Unit.ELF else 3)
                    for u, points in units.items()
                    for p in points
                }
                return run_to_completion(
                    copy.deepcopy(walls),
                    copy.deepcopy(units),
                    unit_data,
                )
            except ElfDiedError:
                pass
        assert False  # Sanity check

    walls, units = parse(input.splitlines())
    return arm_elves(walls, units)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
