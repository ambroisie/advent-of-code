#!/usr/bin/env python

import itertools
import sys
from typing import Iterator, List, Optional


def solve(input: List[str]) -> int:
    def find_illegal_char(input: str) -> Optional[int]:
        chunks: List[str] = []
        ends_to_start = {
            ")": "(",
            "]": "[",
            "}": "{",
            ">": "<",
        }

        for i, c in enumerate(input):
            # Is it a chunk beginning
            if c not in ends_to_start:
                chunks.append(c)
                continue
            # Is it matching the last element on the chunk stack
            current = chunks.pop()
            # If not, corruption has been found
            if ends_to_start[c] != current:
                return i

        return None

    def complete_line(input: str) -> str:
        chunks: List[str] = []
        start_to_end = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">",
        }

        for c in input:
            # Is it a chunk beginning
            if c in start_to_end:
                chunks.append(c)
                continue
            # Otherwise we must match the last open chunk
            assert start_to_end[chunks.pop()] == c  # Sanity check

        return "".join(reversed(list(start_to_end[c] for c in chunks)))

    def score_completion(completion: str) -> int:
        char_score = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4,
        }

        score = 0

        for c in completion:
            score *= 5
            score += char_score[c]

        return score

    def score_completions(completions: Iterator[str]) -> int:
        scores = sorted(map(score_completion, completions))
        return scores[len(scores) // 2]

    incomplete_lines = filter(lambda line: find_illegal_char(line) is None, input)
    completions = map(complete_line, incomplete_lines)

    return score_completions(completions)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
