#!/usr/bin/env python

import sys
from collections import Counter, defaultdict
from typing import NamedTuple


class DateTime(NamedTuple):
    year: int
    month: int
    day: int
    hour: int
    min: int


class Log(NamedTuple):
    datetime: DateTime
    event: str


def solve(input: str) -> int:
    def parse_datetime(input: str) -> DateTime:
        date, time = input.split()
        year, month, day = map(int, date.split("-"))
        hour, min = map(int, time.split(":"))
        return DateTime(year, month, day, hour, min)

    def parse_log(input: str) -> Log:
        date, event = input.split("] ")
        return Log(parse_datetime(date.removeprefix("[")), event)

    def parse(input: list[str]) -> list[Log]:
        return [parse_log(line) for line in input]

    def parse_guard_number(log: Log) -> int:
        assert log.event.startswith("Guard #")  # Sanity check
        assert log.event.endswith(" begins shift")  # Sanity check
        return int(log.event.split()[1].removeprefix("#"))

    def guards_events(logs: list[Log]) -> dict[int, list[Log]]:
        res: dict[int, list[Log]] = defaultdict(list)
        current_guard = parse_guard_number(logs[0])
        for log in logs[1:]:
            if log.event == "falls asleep" or log.event == "wakes up":
                res[current_guard].append(log)
            else:
                current_guard = parse_guard_number(log)
        return res

    def sleep_counts(logs: list[Log]) -> Counter[int]:
        res: Counter[int] = Counter()
        assert len(logs) % 2 == 0  # Sanity check
        for i in range(0, len(logs), 2):
            assert logs[i].event == "falls asleep"  # Sanity check
            assert logs[i + 1].event == "wakes up"  # Sanity check
            start, end = logs[i].datetime, logs[i + 1].datetime
            res.update(range(start.min, end.min))
        return res

    def guard_sleep_counts(
        guard_logs: dict[int, list[Log]],
    ) -> dict[int, Counter[int]]:
        return {guard: sleep_counts(logs) for guard, logs in guard_logs.items()}

    logs = sorted(parse(input.splitlines()))
    guard_logs = guards_events(logs)
    guard_sleeps = guard_sleep_counts(guard_logs)
    most_asleep = max(
        guard_sleeps, key=lambda guard: guard_sleeps[guard].most_common()[0][1]
    )
    return most_asleep * guard_sleeps[most_asleep].most_common()[0][0]


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
