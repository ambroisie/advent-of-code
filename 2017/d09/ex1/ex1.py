#!/usr/bin/env python

import sys
from typing import NamedTuple


class Group(NamedTuple):
    children: list["Group"]


def solve(input: str) -> int:
    def parse_group(input: str) -> tuple[Group, str]:
        garbage = False
        cancel = False
        stack: list[Group] = []
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
                return top, input[i + 1 :]
        assert False  # Sanity check

    def parse(input: str) -> Group:
        group, input = parse_group(input)
        assert not input  # Sanity check
        return group

    def compute_score(group: Group) -> int:
        def helper(group: Group, depth: int) -> int:
            return depth + sum(helper(child, depth + 1) for child in group.children)

        return helper(group, 1)

    groups = parse(input.strip())
    return compute_score(groups)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
