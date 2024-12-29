#!/usr/bin/env python

import sys
from collections import defaultdict
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def solve(input: str) -> int:
    def parse(input: list[str]) -> dict[str, set[str]]:
        graph: dict[str, set[str]] = defaultdict(set)
        for line in input:
            split = line.split()
            prev, after = split[1], split[7]
            graph[after].add(prev)
            graph[prev]  # Ensure that all nodes are in the dictionary
        return graph

    def job_done(graph: dict[str, set[str]], job: str) -> None:
        assert not graph.pop(job)  # Sanity check
        for node in graph:
            graph[node].discard(job)

    def next_job(graph: dict[str, set[str]], ongoing: list[str]) -> str | None:
        return min(
            (n for n, deps in graph.items() if not deps and n not in ongoing),
            default=None,
        )

    def assemble(graph: dict[str, set[str]], additional_time: int, workers: int) -> int:
        res = 0
        worker_time = [0] * workers
        worker_jobs = [""] * workers
        while graph:
            # Step to the next worker, ignoring idle workers, with a default for the first step
            dt = min((t for t in worker_time if t > 0), default=0)
            res += dt
            worker_time = [max(0, t - dt) for t in worker_time]
            for i in range(workers):
                if worker_time[i] != 0:
                    continue
                if worker_jobs[i] != "":
                    job_done(graph, worker_jobs[i])
                    worker_jobs[i] = ""
                if (job := next_job(graph, worker_jobs)) is None:
                    continue
                worker_time[i] = additional_time + ord(job) - ord("A") + 1
                worker_jobs[i] = job
        assert all(j == "" for j in worker_jobs)  # Sanity check
        assert all(t == 0 for t in worker_time)  # Sanity check
        return res

    graph = parse(input.splitlines())
    return assemble(graph, 60, 5)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
