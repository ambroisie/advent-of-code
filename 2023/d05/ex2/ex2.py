#!/usr/bin/env python

import itertools
import sys
from typing import NamedTuple, Optional


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
SeedRanges = list[tuple[int, int]]


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

    def parse(input: str) -> tuple[SeedRanges, Almanac]:
        raw_seeds, *raw_almanac = input.split("\n\n")

        parsed_seed = [int(n) for n in raw_seeds.removeprefix("seeds: ").split(" ")]
        seed_ranges = list(zip(parsed_seed[::2], parsed_seed[1::2]))

        return seed_ranges, parse_almanac(raw_almanac)

    # Each input is piped to exactly one output type, so we can reverse it easily
    def reverse_almanac(almanac: Almanac) -> Almanac:
        def reverse_map_line(line: AlmanacMapLine) -> AlmanacMapLine:
            return AlmanacMapLine(
                dest_start=line.source_start,
                source_start=line.dest_start,
                map_len=line.map_len,
            )

        def reverse_map(map: AlmanacMap) -> AlmanacMap:
            return AlmanacMap([reverse_map_line(line) for line in map.lines])

        reversed: Almanac = {}

        for source, (dest, map) in almanac.items():
            reversed[dest] = source, reverse_map(map)

        return reversed

    def lowest_location(seeds: SeedRanges, inverse_almanac: Almanac) -> int:
        def recurse(input: int, input_type: str) -> Optional[int]:
            if input_type == "seed":
                for start, length in seeds:
                    if start <= input and input < (start + length):
                        return input
                return None

            new_input_type, map = inverse_almanac[input_type]
            return recurse(map.map(input), new_input_type)

        for location in itertools.count():
            if recurse(location, "location") is not None:
                return location
        assert False  # Sanity check

    seeds, almanac = parse(input)
    return lowest_location(seeds, reverse_almanac(almanac))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
