#!/usr/bin/env python

import enum
import functools
import hashlib
import sys
from collections.abc import Callable, Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


# Iteration order of `Direction` is relevant to the solution
class Direction(enum.StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"

    def apply(self, p: Point) -> Point:
        match self:
            case Direction.UP:
                dx, dy = -1, 0
            case Direction.DOWN:
                dx, dy = 1, 0
            case Direction.LEFT:
                dx, dy = 0, -1
            case Direction.RIGHT:
                dx, dy = 0, 1
        return Point(p.x + dx, p.y + dy)


Path = tuple[Direction, ...]


def solve(input: str) -> str:
    def doors_at_passcode(path: Path, passcode: str) -> Iterator[Direction]:
        hashed = hashlib.md5((passcode + "".join(path)).encode()).hexdigest()[:4]
        for c, dir in zip(hashed, Direction):
            if c.isdigit() or c == "a":
                continue
            yield Direction(dir)  # Satisfy Mypy to use the correct return type...

    def bfs(
        start: Point,
        end: Point,
        doors_at: Callable[[Path], Iterator[Direction]],
    ) -> Path:
        queue: list[tuple[Point, Path]] = [(start, ())]

        while queue:
            new_queue: list[tuple[Point, Path]] = []
            for p, path in queue:
                if p == end:
                    return path
                for dir in doors_at(path):
                    new_pos = dir.apply(p)
                    if new_pos.x < 0 or new_pos.x > end.x:
                        continue
                    if new_pos.y < 0 or new_pos.y > end.y:
                        continue
                    new_queue.append((dir.apply(p), path + (dir,)))
            queue = new_queue

        assert False  # Sanity check

    passcode = input.strip()
    doors_at = functools.partial(doors_at_passcode, passcode=passcode)
    return "".join(bfs(Point(0, 0), Point(3, 3), doors_at))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
