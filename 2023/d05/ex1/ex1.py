#!/usr/bin/env python

import sys
from typing import NamedTuple


class AlmanacMapLine(NamedTuple):
    dest_start: int
    source_start: int
    map_len: int


class AlmanacMap(NamedTuple):
    lines: list[AlmanacMapLine]

    def map(self, input: int) -> int:
        for l in self.lines:
            if input < l.source_start:
                continue
            if (l.source_start + l.map_len) <= input:
                continue
            return l.dest_start + (input - l.source_start)
        return input


Almanac = dict[str, tuple[str, AlmanacMap]]


def solve(input: str) -> int:
    def parse_almanac_map_line(line: str) -> AlmanacMapLine:
        dest_start, source_start, map_len = map(int, line.split(" "))
        return AlmanacMapLine(dest_start, source_start, map_len)

    def parse_almanac_map(lines: list[str]) -> tuple[str, str, AlmanacMap]:
        source, dest = lines[0].split(" ")[0].split("-")[::2]

        map_lines = [parse_almanac_map_line(line) for line in lines[1:]]

        return source, dest, AlmanacMap(map_lines)

    def parse_almanac(paragraphs: list[str]) -> Almanac:
        res: Almanac = {}

        for raw_map in paragraphs:
            source, dest, map = parse_almanac_map(raw_map.splitlines())
            res[source] = dest, map

        return res

    def parse(input: str) -> tuple[set[int], Almanac]:
        raw_seeds, *raw_almanac = input.split("\n\n")

        seeds = set(int(n) for n in raw_seeds.removeprefix("seeds: ").split(" "))

        return seeds, parse_almanac(raw_almanac)

    def to_dest(almanac: Almanac, input: int, input_type: str, dest_type: str) -> int:
        if input_type == dest_type:
            return input
        new_input_type, map = almanac[input_type]
        return to_dest(almanac, map.map(input), new_input_type, dest_type)

    seeds, almanac = parse(input)
    return min(to_dest(almanac, seed, "seed", "location") for seed in seeds)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
