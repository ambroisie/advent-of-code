#!/usr/bin/env python

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
    def to_packets(input: str) -> tuple[Packet, Packet]:
        first, second = input.splitlines()
        return eval(first), eval(second)  # Secret best way to parse JSON

    return sum(
        i
        for i, packets in enumerate(input, start=1)
        if cmp_packet(*to_packets(packets)) <= 0
    )


def main() -> None:
    input = sys.stdin.read().split("\n\n")
    print(solve(input))


if __name__ == "__main__":
    main()
