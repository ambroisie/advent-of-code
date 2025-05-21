#!/usr/bin/env python

import sys
from typing import NamedTuple


class RunPerformance(NamedTuple):
    speed: int
    time: int
    rest: int

    def run(self, t: int) -> int:
        cycle_length = self.time + self.rest
        cycles = t // cycle_length
        left_over = t % cycle_length
        run_time = cycles * self.time + min(self.time, left_over)
        return self.speed * run_time


def solve(input: str) -> int:
    def parse_line(input: str) -> tuple[str, RunPerformance]:
        split_input = input.split()
        speed, time, rest = map(int, (split_input[3], split_input[6], split_input[-2]))
        return split_input[0], RunPerformance(speed, time, rest)

    def parse(input: str) -> dict[str, RunPerformance]:
        return {name: perf for name, perf in map(parse_line, input.splitlines())}

    reindeers = parse(input)
    return max(perf.run(2503) for perf in reindeers.values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
