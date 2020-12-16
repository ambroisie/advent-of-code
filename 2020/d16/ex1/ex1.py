#!/usr/bin/env python
import sys
from typing import Dict, List, Set, Tuple

Ranges = Dict[str, Set[int]]
Ticket = List[int]


def parse(raw: List[str]) -> Tuple[Ranges, List[Ticket]]:
    def extract_field_info(line: str) -> Tuple[str, Set[int]]:
        field, rest = line.split(":")
        ranges: Set[int] = set()
        for r in rest.strip().split(" or "):
            lhs, rhs = r.split("-")
            ranges |= set(range(int(lhs), int(rhs) + 1))
        return field, ranges

    def parse_tickets(line: str) -> Ticket:
        return [int(i) for i in line.split(",")]

    ranges: Ranges = {}
    tickets: List[Ticket] = []

    should_parse_tickets = False
    for line in raw:
        if line == "":
            should_parse_tickets = True
            continue
        if "ticket" in line:
            continue
        if should_parse_tickets:
            tickets.append(parse_tickets(line))
        else:
            field, field_ranges = extract_field_info(line)
            ranges[field] = field_ranges

    return ranges, tickets


def solve(raw: List[str]) -> int:
    ranges, tickets = parse(raw)
    sum = 0

    for ticket in tickets[1:]:
        for val in ticket:
            if any(val in r for r in ranges.values()):
                continue
            sum += val

    return sum


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
