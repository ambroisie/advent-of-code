#!/usr/bin/env python

import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional


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


def count_orbits_hop(root: OrbitGraph) -> int:
    nodes: List[OrbitGraph] = []

    def ind_node(node: OrbitGraph) -> int:
        return nodes.index(node)

    def fill_nodes(root: OrbitGraph) -> None:
        nodes.append(root)
        for child in root.children:
            fill_nodes(child)

    fill_nodes(root)
    n = len(nodes)
    dist: List[List[int]] = [[2 * n] * len(nodes) for __ in range(len(nodes))]
    next_nodes: List[List[Optional[OrbitGraph]]] = [[None] * n for __ in range(n)]

    def fill_mat(root: OrbitGraph) -> None:
        # From root to itself
        dist[ind_node(root)][ind_node(root)] = 0
        next_nodes[ind_node(root)][ind_node(root)] = root
        for child in root.children:
            # From root to child
            dist[ind_node(root)][ind_node(child)] = 1
            next_nodes[ind_node(root)][ind_node(child)] = child
            # The other way
            dist[ind_node(child)][ind_node(root)] = 1
            next_nodes[ind_node(child)][ind_node(root)] = root
            # Do it again
            fill_mat(child)

    fill_mat(root)

    for k in range(n):
        print(f"{k} / {n} rounds")
        for i in range(n):
            for j in range(n):
                new_dist = dist[i][k] + dist[k][j]
                if dist[i][j] > new_dist:
                    dist[i][j] = new_dist
                    next_nodes[i][j] = next_nodes[i][k]

    useful_indices: Dict[str, int] = {}
    for index, node in enumerate(nodes):
        if node.name in ("YOU", "SAN"):
            useful_indices[node.name] = index
    return (
        dist[useful_indices["YOU"]][useful_indices["SAN"]] - 2
    )  # Because we are in orbit


def main() -> None:
    print(count_orbits_hop(make_orbits(sys.stdin.readlines())))


if __name__ == "__main__":
    main()
