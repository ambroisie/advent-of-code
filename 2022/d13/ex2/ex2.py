#!/usr/bin/env python

import functools
import sys
from typing import Union

Packet = Union[int, list["Packet"]]


def cmp_packet(lhs: Packet, rhs: Packet) -> int:
    if isinstance(lhs, int) and isinstance(rhs, int):
        return lhs - rhs
    if isinstance(lhs, int):
        lhs = [lhs]
    if isinstance(rhs, int):
        rhs = [rhs]
    non_equal_cmp = (res for res in map(cmp_packet, lhs, rhs) if res != 0)
    len_cmp = cmp_packet(len(lhs), len(rhs))
    return next(non_equal_cmp, len_cmp)


def solve(input: list[str]) -> int:
    def to_packet(input: str) -> Packet:
        # Sanity checks
        assert "\n" not in input
        assert input

        return eval(input)  # Secret best way to parse JSON

    packets = [to_packet(line) for line in input if line]
    packets.extend(
        (
            [[2]],
            [[6]],
        )
    )
    packets.sort(key=functools.cmp_to_key(cmp_packet))

    # Packets are 1-indexed
    first = packets.index([[2]]) + 1
    second = packets.index([[6]]) + 1

    return first * second


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
