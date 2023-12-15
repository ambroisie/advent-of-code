#!/usr/bin/env python

import dataclasses
import sys
from typing import Optional


@dataclasses.dataclass
class Lens:
    label: str
    num: int

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.label == other
        return super().__eq__(other)


def solve(input: list[str]) -> int:
    def compute_hash(string: str) -> int:
        res = 0

        for c in string:
            res += ord(c)
            res *= 17
            res %= 256

        return res

    def parse_step(step: str) -> tuple[str, Optional[int]]:
        if step[-1] == "-":
            return step[:-1], None
        label, num = step.split("=")
        return label, int(num)

    def find_label(label: str, box: list[Lens]) -> Optional[int]:
        for i, lens in enumerate(box):
            if lens.label == label:
                return i
        return None

    def focusing_power(boxes: list[list[Lens]]) -> int:
        res = 0

        for box_num, box in enumerate(boxes, start=1):
            for i, lens in enumerate(box, start=1):
                res += box_num * i * lens.num

        return res

    boxes: list[list[Lens]] = [[] for _ in range(256)]

    for label, num in map(parse_step, input):
        box = compute_hash(label)
        index = find_label(label, boxes[box])
        if num is None:
            # Remove label from box
            if index is not None:
                del boxes[box][index]
        # Place len in box
        elif index is not None:
            boxes[box][index].num = num
        else:
            boxes[box].append(Lens(label, num))

    return focusing_power(boxes)


def main() -> None:
    input = sys.stdin.read().splitlines()
    assert len(input) == 1  # Sanity check
    print(solve(input[0].split(",")))


if __name__ == "__main__":
    main()
