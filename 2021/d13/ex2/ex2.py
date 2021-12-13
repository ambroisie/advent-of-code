#!/usr/bin/env python

import itertools
import sys
from copy import deepcopy
from typing import Iterable, List, Tuple, cast

Paper = List[List[bool]]
Instruction = Tuple[str, int]


def solve(input: List[str]) -> None:
    def transpose(paper: Paper) -> Paper:
        return cast(Paper, list(zip(*paper)))

    def fold_along_y(paper: Paper, y: int) -> Paper:
        assert not any(paper[y])  # Sanity check
        assert y >= len(paper) // 2  # Ensure that we can actually fold the paper

        paper = deepcopy(paper)
        for i, j in zip(itertools.count(y, -1), range(y, len(paper))):
            paper[i] = [(dot_i or dot_j) for dot_i, dot_j in zip(paper[i], paper[j])]

        paper = paper[:y]
        return paper

    def fold_along_x(paper: Paper, x: int) -> Paper:
        return transpose(fold_along_y(transpose(paper), x))

    def do_folds(paper: Paper, instructions: Iterable[Instruction]) -> Paper:
        for axis, n in instructions:
            if axis == "x":
                paper = fold_along_x(paper, n)
            elif axis == "y":
                paper = fold_along_y(paper, n)
            else:
                assert False  # Sanity check

        return paper

    def parse() -> Tuple[Paper, List[Instruction]]:
        paper_part = itertools.takewhile(lambda s: s != "", input)
        fold_part = itertools.islice(
            itertools.dropwhile(lambda s: s != "", input), 1, None
        )

        points = {(int(x), int(y)) for x, y in map(lambda s: s.split(","), paper_part)}
        folds = [
            (axis[-1], int(n)) for axis, n in map(lambda s: s.split("="), fold_part)
        ]

        width, height = max(p[0] for p in points), max(p[1] for p in points)

        paper = [
            [(x, y) in points for x in range(width + 1)] for y in range(height + 1)
        ]

        return paper, folds

    def dump(paper: Paper) -> None:
        for line in paper:
            print("".join("#" if dot else "." for dot in line))

    paper, instructions = parse()

    dump(do_folds(paper, instructions))


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    solve(input)


if __name__ == "__main__":
    main()
