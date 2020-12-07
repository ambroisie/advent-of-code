#!/usr/bin/env python

import re
import sys
from collections import defaultdict
from copy import deepcopy
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


def reverse(graph: Graph) -> Graph:
    reverse: Graph = defaultdict(set)

    for color, contained in graph.items():
        for col in contained:
            reverse[col.color] |= {ColorInfo(-1, color)}

    return reverse


def containing(graph: Graph, col: str) -> Set[ColorInfo]:
    res = deepcopy(graph[col])
    for contains in graph[col]:
        res |= containing(graph, contains.color)
    return res


def solve(raw: List[str]) -> int:
    graph = to_graph(raw)
    reverse_graph = reverse(graph)

    return len(containing(reverse_graph, "shiny gold bag"))


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
