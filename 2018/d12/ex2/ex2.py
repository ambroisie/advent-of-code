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

    def get_diffs(state: str, rules: dict[str, str], iterations: int) -> list[int]:
        res: list[int] = [count_pots(state)]
        prev_count = res[0]
        for _ in range(iterations):
            state = step(state, rules)
            delta = count_pots(state) - prev_count
            prev_count += delta
            res.append(delta)
        return res

    state, rules = parse(input)
    assert len(state) == 100  # Sanity check for `count_pots`

    STEPS = 1000
    deltas = get_diffs(state, rules, STEPS)
    # Change in deltas gets into a steady state after some time
    average_delta = sum(deltas[-100:]) // 100
    return sum(deltas) + (50000000000 - STEPS) * average_delta


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
