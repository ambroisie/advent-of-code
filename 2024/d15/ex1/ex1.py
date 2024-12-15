#!/usr/bin/env python

import copy
import enum
import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Direction(enum.StrEnum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

    def step(self, p: Point) -> Point:
        dx: int
        dy: int

        match self:
            case Direction.UP:
                dx, dy = -1, 0
            case Direction.RIGHT:
                dx, dy = 0, 1
            case Direction.DOWN:
                dx, dy = 1, 0
            case Direction.LEFT:
                dx, dy = 0, -1

        return Point(p.x + dx, p.y + dy)


class Object(enum.StrEnum):
    BOX = "O"
    WALL = "#"


Maze = dict[Point, Object]


def solve(input: str) -> int:
    def parse_maze(input: list[str]) -> tuple[Point, Maze]:
        robot: Point | None = None
        maze: Maze = {}
        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == ".":
                    continue
                if c == "@":
                    robot = Point(x, y)
                    continue
                maze[Point(x, y)] = Object(c)

        assert robot is not None  # Sanity check
        return robot, maze

    def parse_directions(input: str) -> list[Direction]:
        return [Direction(c) for c in input if c in Direction]

    def parse(input: str) -> tuple[Point, Maze, list[Direction]]:
        maze_input, directions_input = input.split("\n\n")
        robot, maze = parse_maze(maze_input.splitlines())
        directions = parse_directions(directions_input)
        return robot, maze, directions

    def step(robot: Point, maze: Maze, d: Direction) -> tuple[Point, Maze]:
        # Maze a tentative step
        new_robot = d.step(robot)
        new_maze = copy.copy(maze)
        # Try to move boxes along
        if (blocker := new_robot) in new_maze:
            # Try to move boxes up
            while blocker in new_maze:
                # We hit a wall, abort the movement
                if new_maze[blocker] == Object.WALL:
                    return robot, maze
                # Otherwise look at the next space along
                blocker = d.step(blocker)
            # Out of the loop, we must have found an empty space, so do the push
            new_maze[blocker] = new_maze.pop(new_robot)
        # Robot moved without hitting a wall
        return new_robot, new_maze

    def compute_coordinates(maze: Maze) -> int:
        return sum(100 * p.x + p.y for p, obj in maze.items() if obj == Object.BOX)

    robot, maze, directions = parse(input)
    for d in directions:
        robot, maze = step(robot, maze, d)
    return compute_coordinates(maze)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
