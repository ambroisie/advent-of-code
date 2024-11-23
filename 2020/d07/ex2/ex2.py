#!/usr/bin/env python

import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass(eq=True, frozen=True)  # Hashable
class ColorInfo:
    num: int
    color: str


Graph = Dict[str, Set[ColorInfo]]


def extract_info(line: str) -> Tuple[str, Set[ColorInfo]]:
    color_pattern = re.compile("(.*) contain ")
    match = color_pattern.search(line)
    assert match is not None
    color = match.group(1).replace("bags", "bag")

    line = line[match.end() : -1]  # Remove period at end of line

    if line == "no other bags":
        return color, set()

    colors: Set[ColorInfo] = set()
    pattern = re.compile("([0-9]+) (.*)")
    for col in line.split(", "):
        match = pattern.search(col)
        assert match is not None
        colors |= {
            ColorInfo(int(match.group(1)), match.group(2).replace("bags", "bag"))
        }

    return color, colors


def to_graph(raw: List[str]) -> Graph:
    return {color: inside for color, inside in map(extract_info, raw)}


def num_bags(graph: Graph, col: str) -> int:
    return sum(
        contained.num * (1 + num_bags(graph, contained.color))
        for contained in graph[col]
    )


def solve(raw: List[str]) -> int:
    graph = to_graph(raw)

    return num_bags(graph, "shiny gold bag")


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
