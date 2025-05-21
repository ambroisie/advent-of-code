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

    def race(reindeers: dict[str, RunPerformance], t: int) -> dict[str, int]:
        points = {name: 0 for name in reindeers.keys()}
        for i in range(1, t + 1):
            # Just re-compute the run every time, it's fast enough
            distances = {name: perf.run(i) for name, perf in reindeers.items()}
            max_dist = max(distances.values())
            for name, distance in distances.items():
                points[name] += distance == max_dist
        return points

    reindeers = parse(input)
    scores = race(reindeers, 2503)
    return max(scores.values())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
