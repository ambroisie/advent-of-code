#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[int, set[int]]:
        origin, others = input.split(" <-> ")
        return int(origin), {int(n) for n in others.split(", ")}

    def parse(input: str) -> dict[int, set[int]]:
        return {n: children for n, children in map(parse_line, input.splitlines())}

    def reachable(graph: dict[int, set[int]]) -> int:
        queue = [0]
        seen: set[int] = set()

        while queue:
            n = queue.pop()
            if n in seen:
                continue
            seen.add(n)
            queue.extend(graph[n])

        return len(seen)

    graph = parse(input)
    return reachable(graph)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
