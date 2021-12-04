#!/usr/bin/env python

import itertools
import sys
from typing import List, Tuple

Board = List[List[int]]


def solve(input: List[str]) -> int:
    def parse_input() -> Tuple[List[int], List[Board]]:
        def listify(line: str, delim: str = " ") -> List[int]:
            return [int(n) for n in line.split(delim) if n != ""]

        draw_order = listify(input[0], delim=",")
        boards: List[Board] = []
        for l in input[1:]:
            if l == "":
                boards.append([])
                continue
            boards[-1].append(listify(l))

        return draw_order, boards

    def bingo(board: Board, draw: List[int]) -> bool:
        assert len(board) == len(board[0])

        def line(l: int) -> bool:
            return all(n in draw for n in board[l])

        def row(r: int) -> bool:
            return all(board[i][r] in draw for i in range(len(board)))

        lines = [line(i) for i in range(len(board))]
        rows = [row(i) for i in range(len(board[0]))]

        return any(itertools.chain(lines, rows))

    draw_order, boards = parse_input()

    draw = []
    losers = set(range(len(boards)))

    for d in draw_order:
        draw.append(d)
        for i, b in enumerate(boards):
            # Stop early if we already know this board wins
            if i not in losers:
                continue
            if not bingo(b, draw):
                continue
            # Discard winners until the last one
            if len(losers) != 1:
                losers.discard(i)
                continue
            # At thid point, we must be looking at the last winning board
            return d * sum(n for n in itertools.chain.from_iterable(b) if n not in draw)

    # Sanity check
    assert False


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
