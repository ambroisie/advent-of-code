#!/usr/bin/env python

import sys


def solve(input: str) -> int:
    def parse(input: str) -> tuple[list[int], list[int]]:
        files: list[int] = []
        free: list[int] = []

        for i, c in enumerate(input):
            if c == "\n":
                continue
            (files if i % 2 == 0 else free).append(int(c))

        # Make `to_disk` slightly simpler
        if len(files) > len(free):
            free.append(0)

        return files, free

    def to_disk(files: list[int], free: list[int]) -> list[int | None]:
        assert len(files) == len(free)  # Sanity check

        disk: list[int | None] = []

        for i in range(len(files)):
            disk.extend([i for _ in range(files[i])])
            disk.extend([None for _ in range(free[i])])

        return disk

    def compact(disk: list[int | None]) -> list[int]:
        last = len(disk) - 1
        for i in range(len(disk)):
            # Are we finished compacting?
            if i >= last:
                break
            # Is this a free space?
            if disk[i] is not None:
                continue
            assert disk[last] is not None  # Sanity check
            disk[i], disk[last] = disk[last], disk[i]
            # Find next block to compact
            while disk[last] is None:
                last -= 1
        # At this point, `None` are at the end
        # Naive list comprehension to appease the type checker
        return [n for n in disk if n is not None]

    files, free = parse(input)
    disk = to_disk(files, free)
    return sum(i * n for i, n in enumerate(compact(disk)))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
