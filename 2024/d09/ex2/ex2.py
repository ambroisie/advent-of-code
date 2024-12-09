#!/usr/bin/env python

import sys
from typing import NamedTuple


class FilePosition(NamedTuple):
    pos: int
    length: int


class ParsedDisk(NamedTuple):
    files: list[FilePosition]
    holes: list[FilePosition]


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

    def to_disk(files: list[int], free: list[int]) -> ParsedDisk:
        assert len(files) == len(free)  # Sanity check

        pos = 0
        disk_files: list[FilePosition] = []
        holes: list[FilePosition] = []

        for i in range(len(files)):
            disk_files.append(FilePosition(pos, files[i]))
            pos += files[i]
            holes.append(FilePosition(pos, free[i]))
            pos += free[i]

        return ParsedDisk(disk_files, holes)

    def compact(disk: ParsedDisk) -> list[int | None]:
        def move_files(disk: ParsedDisk) -> dict[int, FilePosition]:
            new_files: dict[int, FilePosition] = {}
            for i, (pos, length) in reversed(list(enumerate(disk.files))):
                for h in range(len(disk.holes)):
                    # Hole must be big enough to fit the file
                    if length > disk.holes[h].length:
                        continue
                    # Hole must be to the left of the file
                    if pos < disk.holes[h].pos:
                        break
                    # We found a hole, move the file into it
                    pos = disk.holes[h].pos
                    disk.holes[h] = FilePosition(
                        length=disk.holes[h].length - length,
                        pos=disk.holes[h].pos + length,
                    )
                    break
                new_files[i] = FilePosition(pos, length)
            return new_files

        def to_disk(files: dict[int, FilePosition]) -> list[int | None]:
            disk: list[int | None] = [None] * max(
                (f.pos + f.length) for f in files.values()
            )
            for i, f in files.items():
                for j in range(f.length):
                    assert disk[f.pos + j] is None  # Sanity check
                    disk[f.pos + j] = i
            return disk

        new_files = move_files(disk)
        return to_disk(new_files)

    files, free = parse(input)
    disk = to_disk(files, free)
    return sum(i * n for i, n in enumerate(compact(disk)) if n is not None)


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
