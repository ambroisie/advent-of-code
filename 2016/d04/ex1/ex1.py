#!/usr/bin/env python

import collections
import sys
from typing import NamedTuple


class Room(NamedTuple):
    name: str
    sector_id: int
    checksum: str

    def is_real(self) -> bool:
        letters = collections.Counter(self.name.replace("-", ""))
        checksum = sorted(letters.most_common(), key=lambda t: (-t[1], t[0]))[:5]
        return "".join(c for c, _ in checksum) == self.checksum

    @classmethod
    def from_str(cls, input: str) -> "Room":
        input, checksum = map(lambda s: s.removesuffix("]"), input.split("["))
        *name, sector_id = input.split("-")
        return cls("-".join(name), int(sector_id), checksum)


def solve(input: str) -> int:
    def parse(input: str) -> list[Room]:
        return [Room.from_str(line) for line in input.splitlines()]

    rooms = parse(input)
    return sum(room.sector_id for room in rooms if room.is_real())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
