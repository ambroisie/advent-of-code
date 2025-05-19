#!/usr/bin/env python

import collections
import sys


def solve(input: str) -> int:
    def white_elephant(num_elves: int) -> int:
        left = collections.deque(range(1, (num_elves // 2) + 1))
        right = collections.deque(range(num_elves, (num_elves // 2), -1))

        while left and right:
            if len(left) > len(right):
                left.pop()
            else:
                right.pop()
            right.appendleft(left.popleft())
            left.append(right.pop())
        return (left + right)[0]

    num_elves = int(input.strip())
    return white_elephant(num_elves)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
