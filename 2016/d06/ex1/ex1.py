#!/usr/bin/env python

import collections
import sys


def solve(input: str) -> str:
    def error_correct(messages: list[str]) -> str:
        res: list[str] = []
        for i in range(len(messages[0])):
            res.append(collections.Counter(l[i] for l in messages).most_common()[0][0])
        return "".join(res)

    messages = input.splitlines()
    return error_correct(messages)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
