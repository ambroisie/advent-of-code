#!/usr/bin/env python

import enum
import heapq
import sys
from collections import defaultdict
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class ParsedMaze(NamedTuple):
    start: Point
    end: Point
    blocks: set[Point]


class Direction(enum.IntEnum):
    EAST = enum.auto()
    WEST = enum.auto()
    NORTH = enum.auto()
    SOUTH = enum.auto()

    def rotations(self) -> tuple["Direction", "Direction"]:
        match self:
            case Direction.EAST | Direction.WEST:
                return (Direction.NORTH, Direction.SOUTH)
            case Direction.NORTH | Direction.SOUTH:
                return (Direction.EAST, Direction.WEST)

    def step(self, p: Point) -> Point:
        dx: int
        dy: int

        match self:
            case Direction.EAST:
                dx, dy = 0, 1
            case Direction.WEST:
                dx, dy = 0, -1
            case Direction.NORTH:
                dx, dy = -1, 0
            case Direction.SOUTH:
                dx, dy = 1, 0

        return Point(p.x + dx, p.y + dy)


Node = tuple[Point, Direction]


def solve(input: str) -> int:
    def parse(input: list[str]) -> ParsedMaze:
        start: Point | None = None
        end: Point | None = None
        blocks: set[Point] = set()
        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == ".":
                    continue
                p = Point(x, y)
                if c == "S":
                    start = p
                elif c == "E":
                    end = p
                elif c == "#":
                    blocks.add(p)
                else:
                    assert False  # Sanity check
        assert start is not None  # Sanity check
        assert end is not None  # Sanity check
        return ParsedMaze(start, end, blocks)

    def count_path_cells(start: Point, end: Point, blocks: set[Point]) -> int:
        def next_moves(
            pos: Point,
            dir: Direction,
        ) -> Iterator[tuple[int, Point, Direction]]:
            transitions = [(1, dir.step(pos), dir)]
            for new_dir in dir.rotations():
                transitions.append((1000, pos, new_dir))
            for cost, pos, dir in transitions:
                if pos in blocks:
                    continue
                yield cost, pos, dir

        def get_all_predecessors(
            predecessors: dict[Node, set[Node]],
        ) -> set[Point]:
            queue = {(end, dir) for dir in Direction}
            visited: set[Node] = set()
            while queue:
                cur = queue.pop()
                visited.add(cur)
                for pred in predecessors[cur]:
                    if pred in visited:
                        continue
                    queue.add(pred)
            return {p for p, _ in visited}

        # Priority queue of (distance, point)
        queue = [(0, start, Direction.EAST)]
        seen: set[Node] = set()
        predecessors: dict[Node, set[Node]] = defaultdict(set)
        predecessor_cost: dict[Node, int] = {}
        # Use an invalid maximum cost to simplify the loop
        max_cost: int = -1

        while len(queue) > 0:
            cost, p, dir = heapq.heappop(queue)
            # Did we go past the optimal cost, if so stop the loop
            if max_cost > 0 and cost > max_cost:
                break
            # Otherwise, record the minimum cost
            if p == end:
                max_cost = cost
            # We must have seen (p, dir) with a smaller distance before
            if (p, dir) in seen:
                continue
            # First time encountering (p, dir), must be the smallest distance to it
            seen.add((p, dir))
            # Add all neighbours to be visited
            for n_cost, n, n_dir in next_moves(p, dir):
                n_cost += cost
                # Record predecessors
                if predecessor_cost.setdefault((n, n_dir), n_cost) > n_cost:
                    predecessor_cost[(n, n_dir)] = n_cost
                    predecessors[(n, n_dir)] = {(p, dir)}
                elif predecessor_cost[(n, n_dir)] == n_cost:
                    predecessors[(n, n_dir)].add((p, dir))
                heapq.heappush(queue, (n_cost, n, n_dir))

        # Run back up the tree of predecessors to count all cells
        return len(get_all_predecessors(predecessors))

    start, end, blocks = parse(input.splitlines())
    return count_path_cells(start, end, blocks)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()