#!/usr/bin/env python

import sys
from typing import NamedTuple


class Group(NamedTuple):
    children: list["Group"]


def solve(input: str) -> int:
    def parse_group(input: str) -> tuple[Group, str, int]:
        garbage = False
        cancel = False
        stack: list[Group] = []
        total_garbage = 0
        for i, c in enumerate(input):
            if cancel:
                assert garbage  # Sanity check
                cancel = False
                continue
            if garbage:
                if c == "!":
                    cancel = True
                elif c == ">":
                    garbage = False
                else:
                    total_garbage += 1
                continue
            if c == "<":
                garbage = True
                continue
            if c == "{":
                stack.append(Group([]))
                continue
            if c == "}":
                top = stack.pop()
                if stack:
                    stack[-1].children.append(top)
                    continue
                return top, input[i + 1 :], total_garbage
        assert False  # Sanity check

    def parse(input: str) -> tuple[Group, int]:
        groups, input, total_garbage = parse_group(input)
        assert not input  # Sanity check
        return groups, total_garbage

    _, total_garbage = parse(input.strip())
    return total_garbage


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
