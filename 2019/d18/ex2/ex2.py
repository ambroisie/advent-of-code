#!/usr/bin/env python
import heapq
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache
from math import inf
from typing import DefaultDict, Deque, Dict, FrozenSet, Iterator, List, Tuple, Union

RawGrid = List[str]
GraphInfo = List[Tuple[str, int]]
Graph = Dict[str, GraphInfo]


@dataclass(eq=True, frozen=True)  # Hash-able
class Position:
    x: int
    y: int


def neighbours(grid: RawGrid, pos: Position) -> Iterator[Position]:
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        new_pos = Position(pos.x + dx, pos.y + dy)
        if not (0 <= new_pos.x < len(grid) and 0 <= new_pos.y < len(grid[0])):
            continue
        if grid[new_pos.x][new_pos.y] == "#":
            continue
        yield new_pos


def find_adjacent(grid: RawGrid, pos: Position) -> GraphInfo:
    queue: Deque[Tuple[Position, int]] = deque()
    visited = {pos}
    adjacent: GraphInfo = []

    for n in neighbours(grid, pos):
        queue.append((n, 1))  # Distance is 1

    while queue:
        n, d = queue.popleft()
        if n in visited:
            continue
        visited |= {n}
        cell = grid[n.x][n.y]

        if cell not in "#.1234":  # We don't care about those
            adjacent.append((cell, d))
            continue  # Do not go through doors and keys

        for neighbour in neighbours(grid, n):
            queue.append((neighbour, d + 1))

    return adjacent


def build_graph(grid: RawGrid) -> Graph:
    graph = {}

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell not in "#.":
                graph[cell] = find_adjacent(grid, Position(x, y))

    return graph


def solve(G: Graph, start: str) -> int:
    @lru_cache(2 ** 20)
    def reachable_keys(src: str, found: FrozenSet[str]) -> GraphInfo:
        queue = []
        distance: DefaultDict[str, Union[float, int]] = defaultdict(lambda: inf)
        reachable: GraphInfo = []

        for neighbor, weight in G[src]:
            queue.append((weight, neighbor))  # Weight first for heap comparisons

        heapq.heapify(queue)

        while queue:
            dist, node = heapq.heappop(queue)

            # Do key, add it to reachable if not found previously
            if node.islower() and node not in found:
                reachable.append((node, dist))
                continue

            # Do door, if not opened by a key that was found in the search
            if node.lower() not in found:
                continue

            # If not a key and not a closed door
            for neighbor, weight in G[node]:
                new_dist = dist + weight
                if new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    heapq.heappush(queue, (new_dist, neighbor))

        return reachable

    @lru_cache(2 ** 20)
    def min_steps(
        sources: str, keys_to_find: int, found: FrozenSet[str] = frozenset()
    ) -> Union[float, int]:
        if keys_to_find == 0:
            return 0

        best = inf

        for src in sources:
            for key, dist in reachable_keys(src, found):
                new_keys = found | {key}
                new_sources = sources.replace(src, key)
                new_dist = dist + min_steps(new_sources, keys_to_find - 1, new_keys)

                if new_dist < best:
                    best = new_dist

        return best

    total_keys = sum(node.islower() for node in G)
    return int(min_steps(start, total_keys))  # Throw if we kept the infinite float


def main() -> None:
    G = build_graph(list(line.strip() for line in sys.stdin.readlines()))
    print(solve(G, "1234"))


if __name__ == "__main__":
    main()
