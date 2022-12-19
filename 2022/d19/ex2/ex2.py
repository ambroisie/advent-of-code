#!/usr/bin/env python

import dataclasses
import enum
import itertools
import math
import sys
from collections import deque
from collections.abc import Iterable, Iterator, Mapping
from typing import NamedTuple, Optional, TypeVar

T = TypeVar("T")


def grouper(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip(*args, strict=True)


class Resource(str, enum.Enum):
    GEODE = "geode"
    OBSIDIAN = "obsidian"
    CLAY = "clay"
    ORE = "ore"


class ResourceCost(Mapping[Resource, int]):
    _dict: dict[Resource, int]
    _hash: Optional[int]

    def __init__(self, init: Mapping[Resource, int] = {}, /) -> None:
        self._dict = {res: init.get(res, 0) for res in Resource}
        self._hash = None

        assert all(self._dict[res] >= 0 for res in Resource)  # Sanity check

    def __getitem__(self, key: Resource, /) -> int:
        return self._dict[key]

    def __iter__(self) -> Iterator[Resource]:
        return iter(Resource)  # Always use same Resource iteration order

    def __len__(self) -> int:
        return len(self._dict)

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(tuple(sorted(self._dict)))
        return self._hash

    def __add__(self, other):
        if not isinstance(other, ResourceCost):
            return NotImplemented
        return ResourceCost({res: self[res] + other[res] for res in Resource})

    def __sub__(self, other):
        if not isinstance(other, ResourceCost):
            return NotImplemented
        return ResourceCost({res: self[res] - other[res] for res in Resource})

    def __repr__(self) -> str:
        return repr(self._dict)

    def has_enough(self, costs: "ResourceCost") -> bool:
        return all(self[res] >= costs[res] for res in Resource)


@dataclasses.dataclass
class Blueprint:
    construction_costs: dict[Resource, ResourceCost]

    @classmethod
    def from_input(cls, input: str) -> "Blueprint":
        assert input.startswith("Blueprint ")  # Sanity check

        raw_costs = input.split(": ")[1].split(". ")
        costs: dict[Resource, ResourceCost] = {}
        for raw in map(str.split, raw_costs):
            ressource = Resource(raw[1])
            costs[ressource] = ResourceCost(
                {
                    Resource(r.removesuffix(".")): int(c)
                    for c, r in grouper((w for w in raw[4:] if w != "and"), 2)
                }
            )

        return cls(costs)

    def maximize_geodes(self, run_time: int) -> int:
        class QueueNode(NamedTuple):
            time: int
            robots: ResourceCost
            inventory: ResourceCost
            total_mined: ResourceCost

        def prune_queue(queue: Iterable[QueueNode]) -> deque[QueueNode]:
            def priority_key(node: QueueNode) -> int:
                MULTIPLIERS = {
                    Resource.GEODE: 1_000_000,
                    Resource.OBSIDIAN: 10_000,
                    Resource.CLAY: 100,
                    Resource.ORE: 1,
                }
                return sum(
                    node.total_mined[res] * mul for res, mul in MULTIPLIERS.items()
                )

            MAX_QUEUE = 10_000  # Chosen arbitrarily
            return deque(sorted(queue, key=priority_key, reverse=True)[:MAX_QUEUE])

        def do_build(node: QueueNode, robot_type: Optional[Resource]) -> QueueNode:
            costs = (
                self.construction_costs[robot_type]
                if robot_type is not None
                else ResourceCost()
            )
            assert node.inventory.has_enough(costs)  # Sanity check
            new_robots = node.robots + (
                ResourceCost({robot_type: 1})
                if robot_type is not None
                else ResourceCost()
            )
            new_inventory = node.inventory + node.robots - costs
            new_total_mined = node.total_mined + node.robots
            return QueueNode(node.time + 1, new_robots, new_inventory, new_total_mined)

        max_geode = 0

        queue: deque[QueueNode] = deque(
            # Starting conditions
            [
                QueueNode(
                    0, ResourceCost({Resource.ORE: 1}), ResourceCost(), ResourceCost()
                )
            ]
        )
        dfs_depth = 0
        while queue:
            node = queue.popleft()

            if node.time > dfs_depth:
                # An awful hack to reduce the search space and prioritize geodes
                queue = prune_queue(queue)
                dfs_depth = node.time

            if node.time == run_time:
                max_geode = max(max_geode, node.total_mined[Resource.GEODE])
                continue

            # Try building a robot
            for robot_type in itertools.chain(Resource):
                costs = self.construction_costs[robot_type]
                # Don't build robots we can't afford
                if not node.inventory.has_enough(costs):
                    continue
                # Don't build robots when already producing more than enough
                if robot_type != Resource.GEODE and all(
                    c[robot_type] <= node.robots[robot_type]
                    for c in self.construction_costs.values()
                ):
                    continue
                queue.append(do_build(node, robot_type))
            # Try not building anything
            queue.append(do_build(node, None))

        return max_geode


def solve(input: list[str]) -> int:
    blueprints = [Blueprint.from_input(line) for line in input]

    TIME = 32

    return math.prod(blueprint.maximize_geodes(TIME) for blueprint in blueprints[:3])


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
