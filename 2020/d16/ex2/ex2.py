#!/usr/bin/env python
import math
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


def verify_mapping(possibilites: Dict[int, Set[str]]) -> None:
    for pos in possibilites.values():
        assert len(pos) == 1


def cross_eliminate(possibilites: Dict[int, Set[str]]) -> None:
    while True:
        eliminated = False
        for pos in possibilites:
            if len(possibilites[pos]) != 1:
                continue
            for other_pos in possibilites:
                if other_pos == pos:
                    continue
                if len(possibilites[other_pos] & possibilites[pos]) == 0:
                    continue
                eliminated = True
                possibilites[other_pos] = possibilites[other_pos] - (possibilites[pos])
        if not eliminated:
            break


def match_ranges(ranges: Ranges, tickets: List[Ticket]) -> Dict[int, str]:
    possibilites: Dict[int, Set[str]] = {
        i: set(ranges.keys()) for i in range(len(ranges))
    }

    def whittle_down() -> None:
        for t in tickets[1:]:
            for i, val in enumerate(t):
                for field, valid in ranges.items():
                    if val in valid:
                        continue
                    possibilites[i].remove(field)

    whittle_down()
    cross_eliminate(possibilites)
    verify_mapping(possibilites)

    return {i: pos.pop() for i, pos in possibilites.items()}


def solve(raw: List[str]) -> int:
    ranges, tickets = parse(raw)

    def valid(t: Ticket) -> bool:
        for val in t:
            if not any(val in r for r in ranges.values()):
                return False
        return True

    tickets = [t for i, t in enumerate(tickets) if i == 0 or valid(t)]

    mapping = match_ranges(ranges, tickets)
    return math.prod(
        tickets[0][i] for i, field in mapping.items() if "departure" in field
    )


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
