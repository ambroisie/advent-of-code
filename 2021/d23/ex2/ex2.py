#!/usr/bin/env python

import enum
import functools
import sys
from typing import Iterator, List, NamedTuple, Optional, Tuple, cast


class Point(NamedTuple):
    x: int
    y: int


class Amphipod(enum.IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3


class Direction(enum.IntEnum):
    ALLEY = 0
    ROOM = 1


# 7-length tuple, but easier for mypy in a variadic type
Alley = Tuple[Optional[Amphipod], ...]

# Actually variadic tuple, instead of a list, for memoization purposes
Room = Tuple[Amphipod, ...]

# 4-length tuple, but easier for mypy in a variadic type
Rooms = Tuple[Room, ...]


class Board(NamedTuple):
    alley: Alley
    rooms: Rooms


class Move(NamedTuple):
    cost: int
    new_board: Board


FUEL_COST = {
    Amphipod.A: 1,
    Amphipod.B: 10,
    Amphipod.C: 100,
    Amphipod.D: 1000,
}

DISTANCE = [
    # From room 1
    (2, 1, 1, 3, 5, 7, 8),
    # From room 2
    (4, 3, 1, 1, 3, 5, 6),
    # From room 3
    (6, 5, 3, 1, 1, 3, 4),
    # From room 4
    (8, 7, 5, 3, 1, 1, 2),
]

AMPHIPOD_FROM_STRING = {
    "A": Amphipod.A,
    "B": Amphipod.B,
    "C": Amphipod.C,
    "D": Amphipod.D,
}

ROOM_SIZE = 4


def solve(input: List[str]) -> int:
    def parse() -> Board:
        def adjust_board(board: Board) -> Board:
            rooms: Rooms = ()
            ADDITIONAL = (
                (Amphipod.D, Amphipod.D),
                (Amphipod.C, Amphipod.B),
                (Amphipod.B, Amphipod.A),
                (Amphipod.A, Amphipod.C),
            )
            for i, room in enumerate(board.rooms):
                rooms = rooms + (room[:1] + ADDITIONAL[i] + room[1:],)
            return Board(board.alley, rooms)

        alley: Alley = (None,) * 7
        rooms: Rooms = ()
        for i in (3, 5, 7, 9):
            room: Room = tuple(
                AMPHIPOD_FROM_STRING[input[j][i]] for j in range(2, 3 + 1)
            )
            rooms = rooms + (room,)

        return adjust_board(Board(alley, rooms))

    def room_is_solved(board: Board, amphipod: Amphipod) -> bool:
        room = board.rooms[amphipod]
        return len(room) == ROOM_SIZE and all(a == amphipod for a in room)

    def board_is_solved(board: Board) -> bool:
        return all(room_is_solved(board, Amphipod(i)) for i in range(len(board.rooms)))

    def move_cost(
        board: Board, room: int, alley_spot: int, direction: Direction
    ) -> Optional[int]:
        # Going left-to-right, or right-to-left
        if room < (alley_spot - 1):
            alley_start = room + 2
            # Look at the end spot if we're going to the alley, not if we come from there
            alley_end = alley_spot + (1 - direction)
        else:
            # Look at the first spot if we're going to the alley, not if we come from there
            alley_start = alley_spot + direction
            alley_end = room + 2

        # Is there any obstacle in the way
        if any(spot is not None for spot in board.alley[alley_start:alley_end]):
            return None

        amphipod = (
            board.alley[alley_spot]
            if direction == Direction.ROOM
            else board.rooms[room][0]
        )
        assert amphipod is not None  # Sanity check

        return FUEL_COST[amphipod] * (
            DISTANCE[room][alley_spot] + direction + ROOM_SIZE - len(board.rooms[room])
        )

    # Yes this returns a 0-or-1 length iterator, but it's practical for `moves`
    def alley_moves_for(board: Board, i: int) -> Iterator[Move]:
        # Return early if we're trying to move out of an empty spot
        spot = board.alley[i]
        if spot is None:
            return

        # Can't yet move to the target room if any amphipod is out of place there
        if any(other != spot for other in board.rooms[spot]):
            return

        cost = move_cost(board, spot, i, Direction.ROOM)

        # Can't move there yet, there's an obstacle in the way
        if cost is None:
            return

        # Update the board state
        alley, rooms = board
        rooms = rooms[:spot] + ((spot,) + rooms[spot],) + rooms[spot + 1 :]
        alley = alley[:i] + (None,) + alley[i + 1 :]

        yield Move(cost, Board(alley, rooms))

    def rooms_moves_for(board: Board, i: int) -> Iterator[Move]:
        room = board.rooms[i]
        # No need to move out of a solved room
        if all(a == i for a in room):
            return

        for dest in range(len(board.alley)):
            cost = move_cost(board, i, dest, Direction.ALLEY)

            # Can't move there yet, there's an obstacle in the way
            if cost is None:
                continue

            # Update the board state
            alley, rooms = board
            rooms = rooms[:i] + (room[1:],) + rooms[i + 1 :]
            alley = alley[:dest] + (room[0],) + alley[dest + 1 :]

            yield Move(cost, Board(alley, rooms))

    def moves(board: Board) -> Iterator[Move]:
        for i in range(len(board.alley)):
            yield from alley_moves_for(board, i)
        for i in range(len(board.rooms)):
            yield from rooms_moves_for(board, i)

    @functools.cache
    def total_cost(board: Board) -> Optional[int]:
        if board_is_solved(board):
            return 0

        best = None

        for cost, new_board in moves(board):
            if (end_cost := total_cost(new_board)) is None:
                continue
            cost += end_cost
            if best is None or cost < best:
                best = cost

        return best

    board = parse()
    cost = total_cost(board)
    assert cost is not None  # Sanity check

    return cost


def main() -> None:
    input = [line.rstrip("\n") for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
