#!/usr/bin/env python

import sys
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class OrbitGraph:
    name: str
    children: List["OrbitGraph"] = field(default_factory=list)


def make_orbits(description: List[str]) -> OrbitGraph:
    orbits: Dict[str, OrbitGraph] = {}

    def find_or_add(name: str) -> OrbitGraph:
        if name in orbits:
            return orbits[name]
        orbit = OrbitGraph(name)
        orbits[name] = orbit
        return orbit

    for l in description:
        parent, child = map(find_or_add, map(lambda x: x.strip(), l.split(")")))
        parent.children.append(child)

    return orbits["COM"]  # Assume common root is named 'COM'


def count_orbits(root: OrbitGraph) -> int:
    ans = 0
    stack = 0  # Count the number of direct and indirect orbits to the current root

    def helper(root: OrbitGraph):
        nonlocal ans
        nonlocal stack
        ans += stack  # Count the number of orbits to this node
        stack += 1  # Add the current root to stack of parents
        for child in root.children:
            helper(child)  # Count those orbits for each child
        stack -= 1  # Remove the current root from the stack of parents

    helper(root)
    return ans


def main() -> None:
    print(count_orbits(make_orbits(sys.stdin.readlines())))


if __name__ == "__main__":
    main()
