#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse_rules(input: list[str]) -> dict[str, str]:
        return {key: val for key, val in map(lambda s: s.split(" => "), input)}

    def parse(input: str) -> tuple[str, dict[str, str]]:
        init, rules = input.split("\n\n")
        return init.split(": ")[1], parse_rules(rules.splitlines())

    def step(state: str, rules: dict[str, str]) -> str:
        state = "...." + state + "...."
        return "".join(
            rules.get(state[i - 2 : i + 2 + 1], ".") for i in range(2, len(state) - 2)
        )

    def count_pots(state: str) -> int:
        return sum(
            i for i, c in enumerate(state, start=-(len(state) - 100) // 2) if c == "#"
        )

    state, rules = parse(input)
    assert len(state) == 100  # Sanity check for `count_pots`
    for _ in range(20):
        state = step(state, rules)
    return count_pots(state)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
