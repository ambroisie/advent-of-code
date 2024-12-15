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


# Maze always contains the left part of the object
Maze = dict[Point, Object]
# WideMaze maps left and right side of an object to its (left, right) tuple
WideMaze = dict[Point, tuple[Point, Point]]


def solve(input: str) -> int:
    def parse_maze(input: list[str]) -> tuple[Point, Maze]:
        robot: Point | None = None
        maze: Maze = {}
        for x, line in enumerate(input):
            for y, c in enumerate(line):
                if c == ".":
                    continue
                if c == "@":
                    robot = Point(x, y * 2)
                    continue
                maze[Point(x, y * 2)] = Object(c)

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
        def widen_maze() -> WideMaze:
            res: WideMaze = {}
            for p in maze.keys():
                right_p = Point(p.x, p.y + 1)
                res[p] = (p, right_p)
                res[right_p] = (p, right_p)
            return res

        def boxes_along(wide_maze: WideMaze) -> set[Point] | None:
            def helper(current: Point) -> set[Point] | None:
                # Return empty set if we hit the air
                if current not in wide_maze:
                    return set()

                # Query both sides of the object
                left, right = wide_maze[current]

                # Return None if we hit a wall
                if maze[left] == Object.WALL:
                    return None
                assert right not in maze  # Sanity check

                # Try to move both sides of the box recursively
                res_left: set[Point] = set()
                res_right: set[Point] = set()
                # Only check next_left if not moving right
                if (next_left := d.step(left)) != right:
                    if (try_left := helper(next_left)) is None:
                        return None
                    res_left = try_left
                # And only check next_right if not moving left
                if (next_right := d.step(right)) != left:
                    if (try_right := helper(next_right)) is None:
                        return None
                    res_right = try_right

                # Both sides succeeded, return the set of boxes to move
                return {left} | res_left | res_right

            return helper(d.step(robot))

        def move_boxes(boxes: set[Point]) -> Maze:
            new_maze = copy.copy(maze)
            # Do the move in two steps to avoid overwriting any values during movement
            for box in boxes:
                new_maze.pop(box)
            for box in boxes:
                new_maze[d.step(box)] = maze[box]
            return new_maze

        new_robot = d.step(robot)
        # If we hit a wall, abort the step
        if maze.get(new_robot) == Object.WALL:
            return robot, maze
        # If a box hits a wall, abort the step
        if (boxes := boxes_along(widen_maze())) is None:
            return robot, maze
        # Otherwise move everything along the direction
        return new_robot, move_boxes(boxes)

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
