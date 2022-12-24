#!/usr/bin/env python

import dataclasses
import enum
import sys
from collections import defaultdict, deque
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)


class Direction(str, enum.Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def to_delta(self) -> Point:
        match self:
            case Direction.UP:
                return Point(-1, 0)
            case Direction.DOWN:
                return Point(1, 0)
            case Direction.LEFT:
                return Point(0, -1)
            case Direction.RIGHT:
                return Point(0, 1)


@dataclasses.dataclass
class ValleyMap:
    start: Point
    goal: Point
    valley_corners: tuple[Point, Point]
    tornadoes: dict[Point, Direction]

    @classmethod
    def from_input(cls, input: list[str]) -> "ValleyMap":
        tornadoes: dict[Point, Direction] = {}
        for x, line in enumerate(input, start=1):
            for y, c in enumerate(line, start=1):
                if c in ("#", "."):
                    continue
                tornadoes[Point(x, y)] = Direction(c)
        return cls(
            # Start position is always above the upper left corner of valley
            start=Point(1, 2),
            # Goal position is always under the lower left corner of valley
            goal=Point(len(input), len(input[0]) - 1),
            # Valley is surrounded by walls, except entrance and exit
            valley_corners=(Point(2, 2), Point(len(input) - 1, len(input[0]) - 1)),
            tornadoes=tornadoes,
        )

    def _is_in_valley(self, p: Point) -> bool:
        # Valley also includes start/end
        if p in (self.start, self.goal):
            return True
        # Otherwise, just do a bounds check for inside the walls
        ((minx, miny), (maxx, maxy)) = self.valley_corners
        return (minx <= p.x <= maxx) and (miny <= p.y <= maxy)

    def _wrap_tornado(self, p: Point) -> Point:
        if self._is_in_valley(p):
            return p
        x, y = p
        h = self.valley_corners[1].x - self.valley_corners[0].x + 1
        w = self.valley_corners[1].y - self.valley_corners[0].y + 1
        if x == 1:
            x += h
        if y == 1:
            y += w
        if x > self.valley_corners[1].x:
            x -= h
        if y > self.valley_corners[1].y:
            y -= w
        return Point(x, y)

    def navigate(self) -> int:
        TornadoesMap = dict[Point, list[Direction]]

        def move_tornadoes(map: TornadoesMap) -> dict[Point, list[Direction]]:
            res: dict[Point, list[Direction]] = defaultdict(list)
            for p, tornadoes in map.items():
                for t in tornadoes:
                    new_pos = self._wrap_tornado(p + t.to_delta())
                    res[new_pos].append(t)
            return dict(res)

        def moves(p: Point) -> Iterator[Point]:
            yield p
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                yield p + Point(dx, dy)

        # Do a BFS to find the fastest route
        queue: deque[tuple[int, Point]] = deque([(0, self.start)])
        seen: set[tuple[int, Point]] = set()
        tornado_history = [{p: [t] for p, t in self.tornadoes.items()}]
        while queue:
            dist, pos = queue.popleft()
            # If goal found, return total distance
            if pos == self.goal:
                return dist
            # Check that we don't do redundant work
            if (dist, pos) in seen:
                continue
            seen.add((dist, pos))
            if len(tornado_history) <= (dist + 1):
                tornado_history.append(move_tornadoes(tornado_history[-1]))
            for new_pos in moves(pos):
                # Can't move into the walls, but can move in start/end
                if not self._is_in_valley(new_pos):
                    continue
                # Can't occupy same space as tornadoes
                if new_pos in tornado_history[dist + 1]:
                    continue
                # Enqueue this move to the search space
                queue.append((dist + 1, new_pos))
        assert False  # Sanity check


def solve(input: list[str]) -> int:
    valley = ValleyMap.from_input(input)
    return valley.navigate()


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
