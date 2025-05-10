#!/usr/bin/env python

import sys
from typing import NamedTuple


class Spin(NamedTuple):
    n: int


class Exchange(NamedTuple):
    a: int
    b: int


class Partner(NamedTuple):
    a: str
    b: str


Move = Spin | Exchange | Partner

Programs = tuple[str, ...]


def solve(input: str) -> str:
    def parse_move(input: str) -> Move:
        if input[0] == "s":
            return Spin(int(input[1:]))
        if input[0] == "x":
            return Exchange(*map(int, input[1:].split("/")))
        if input[0] == "p":
            return Partner(*input[1:].split("/"))
        assert False  # Sanity check

    def parse(input: str) -> list[Move]:
        return [parse_move(move) for move in input.strip().split(",")]

    def apply_move(programs: Programs, move: Move) -> Programs:
        match move:
            case Spin(n):
                return programs[-n:] + programs[:-n]
            case Exchange(a, b):
                tmp = list(programs)
                tmp[a], tmp[b] = tmp[b], tmp[a]
                return tuple(tmp)
            case Partner(a, b):
                ia, ib = programs.index(a), programs.index(b)
                tmp = list(programs)
                tmp[ia], tmp[ib] = tmp[ib], tmp[ia]
                return tuple(tmp)

    def do_dance(programs: Programs, moves: list[Move]) -> Programs:
        t = 0
        cache = {(programs, 0): 0}
        TOTAL_MOVES = 1000000000 * len(moves)
        while t < TOTAL_MOVES:
            programs = apply_move(programs, moves[t % len(moves)])
            t += 1
            key = (programs, t % len(moves))
            if (previous_t := cache.get(key)) is not None:
                cycle_length = t - previous_t
                num_cycles = (TOTAL_MOVES - t) // cycle_length
                t += num_cycles * cycle_length
            else:
                cache[key] = t

        return programs

    moves = parse(input)
    programs = tuple(chr(ord("a") + i) for i in range(16))
    programs = do_dance(programs, moves)
    return "".join(programs)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
