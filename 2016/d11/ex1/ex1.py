#!/usr/bin/env python

import dataclasses
import heapq
import itertools
import sys
from collections.abc import Iterator
from typing import NamedTuple

NUM_FLOORS = 4


@dataclasses.dataclass(frozen=True)
class Microchip:
    element: str


@dataclasses.dataclass(frozen=True)
class Generator:
    element: str


Item = Microchip | Generator


@dataclasses.dataclass(frozen=True, order=True)
class State:
    class Floor(NamedTuple):
        chip: int
        generator: int

    elevator: int
    items: tuple[Floor, ...]

    def __post_init__(self) -> None:
        assert self.items == tuple(sorted(self.items))  # Sanity check


def solve(input: str) -> int:
    def parse_item(input: str) -> Item:
        _, element, item_type = input.split()
        if item_type == "microchip":
            return Microchip(element.removesuffix("-compatible"))
        elif item_type == "generator":
            return Generator(element)
        assert False  # Sanity check

    def parse_floor(input: str) -> list[Item]:
        # Simplify parsing, and remove `The Xth floor contains`
        input = input.removesuffix(".").replace(", and ", ", ").replace(" and ", ", ")
        input = " ".join(input.split()[4:])
        if input == "nothing relevant":
            return []
        return [parse_item(it) for it in input.split(", ")]

    def parse(input: str) -> dict[Item, int]:
        return {
            it: i
            for i, line in enumerate(input.splitlines())
            for it in parse_floor(line)
        }

    def to_state(elevator: int, floors: dict[Item, int]) -> State:
        elements = {it.element for it in floors}
        return State(
            elevator=elevator,
            items=tuple(
                sorted(
                    State.Floor(floors[Microchip(elem)], floors[Generator(elem)])
                    for elem in elements
                )
            ),
        )

    def from_state(state: State) -> tuple[int, dict[Item, int]]:
        floors: dict[Item, int] = {}
        for i, (chip, generator) in enumerate(state.items):
            floors[Microchip(str(i))] = chip
            floors[Generator(str(i))] = generator
        return state.elevator, floors

    def solve(state: State) -> int:
        def items_at(
            item_type: type[Item],
            floor: int,
            items: dict[Item, int],
        ) -> set[str]:
            return {
                it.element
                for it, it_floor in items.items()
                if it_floor == floor and isinstance(it, item_type)
            }

        def neighbours(state: State) -> Iterator[State]:
            elevator, all_items = from_state(state)
            chips = items_at(Microchip, elevator, all_items)
            gens = items_at(Generator, elevator, all_items)
            for dest_floor in (elevator - 1, elevator + 1):
                # Don't move the elevator out of bounds
                if dest_floor < 0 or dest_floor >= NUM_FLOORS:
                    continue

                dest_chips = items_at(Microchip, dest_floor, all_items)
                dest_gens = items_at(Generator, dest_floor, all_items)
                unmatched_chips = dest_chips - dest_gens
                if unmatched_chips:
                    assert not dest_gens  # Sanity check

                single_items: list[Item] = []
                # Chips
                for chip in chips:
                    # can move to floors with no generator, or a matching generator
                    if dest_gens and chip not in dest_gens:
                        continue
                    single_items.append(Microchip(chip))
                # Generators
                for gen in gens:
                    # can move to floors without unmatched chips or only their chip
                    if unmatched_chips - {gen}:
                        continue
                    # ... but only if they're not currently protecting their chip
                    if gen in chips and gens - {gen}:
                        continue
                    single_items.append(Generator(gen))

                double_items: list[tuple[Item, Item]] = []
                # Two chips
                for chip1, chip2 in itertools.combinations(chips, 2):
                    # Can move to floors with no generator, or both matching generators
                    if dest_gens and not dest_gens.issuperset({chip1, chip2}):
                        continue
                    double_items.append((Microchip(chip1), Microchip(chip2)))
                # Two generators
                for gen1, gen2 in itertools.combinations(gens, 2):
                    # Can move to floors with unmatched chips, if they match them...
                    if unmatched_chips - {gen1, gen2}:
                        continue
                    # ... but only if they're not currently protecting their chip
                    if (gen1 in chips or gen2 in chips) and gens - {gen1, gen2}:
                        continue
                    double_items.append((Generator(gen1), Generator(gen2)))
                # Matching generator and chip
                for match in chips & gens:
                    # Can move to floors with no unmatched chips
                    if not unmatched_chips:
                        double_items.append((Microchip(match), Generator(match)))

                for item in single_items:
                    new_items = all_items | {item: dest_floor}
                    assert new_items.keys() == all_items.keys()  # Sanity check
                    yield to_state(dest_floor, new_items)
                for item1, item2 in double_items:
                    new_items = all_items | {item1: dest_floor, item2: dest_floor}
                    assert new_items.keys() == all_items.keys()  # Sanity check
                    yield to_state(dest_floor, new_items)

        def dijkstra(start: State, end: State) -> int:
            # Priority queue of (distance, point)
            queue = [(0, start)]
            seen: set[State] = set()

            while len(queue) > 0:
                dist, p = heapq.heappop(queue)
                if p == end:
                    return dist
                # We must have seen p with a smaller distance before
                if p in seen:
                    continue
                # First time encountering p, must be the smallest distance to it
                seen.add(p)
                # Add all neighbours to be visited
                for n in neighbours(p):
                    heapq.heappush(queue, (dist + 1, n))

            assert False  # Sanity check

        # On the end state, we want all items pairs on the top floor
        # The elevator must be on the top floor as well to get the last item up
        top = NUM_FLOORS - 1
        end = State(top, tuple(State.Floor(top, top) for _ in state.items))
        return dijkstra(state, end)

    floors = parse(input)
    state = to_state(0, floors)
    return solve(state)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
