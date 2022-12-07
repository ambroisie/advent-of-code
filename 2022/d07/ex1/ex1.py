#!/usr/bin/env python

import sys
from typing import Union

FileSystem = dict[str, Union[int, "FileSystem"]]


def solve(input: list[str]) -> int:
    def build_tree(input: list[str], i: int = 0) -> tuple[FileSystem, int]:

        fs: FileSystem = {}

        while i < len(input):
            assert input[i][0] == "$"  # Sanity check
            command = input[i].split()[1:]
            if command[0] == "ls":
                while (i := i + 1) < len(input):
                    if input[i][0] == "$":
                        break
                    else:
                        type, name = input[i].split()
                        if type == "dir":
                            continue
                        fs[name] = int(type)
            elif command[0] == "cd":
                if command[1] == "..":
                    i += 1
                    break
                else:
                    fs[command[1]], i = build_tree(input, i + 1)
            else:
                assert False  # Sanity check

        return fs, i

    def total_size(
        fs: FileSystem, parent_path: str = ""
    ) -> dict[str, tuple[int, bool]]:
        sizes: dict[str, tuple[int, bool]] = {}

        for f, content in fs.items():
            path = f"{parent_path}/{f}"
            if isinstance(content, int):
                sizes[path] = content, False
            elif isinstance(content, dict):
                children_sizes = total_size(content, path)
                total = sum(children_sizes[f"{path}/{c}"][0] for c in content.keys())
                sizes[path] = total, True
                sizes.update(children_sizes)
            else:
                assert False  # Sanity check

        return sizes

    fs, i = build_tree(input)
    assert i == len(input)  # Sanity check
    sizes = total_size(fs)
    THRESHOLD = 100000
    return sum(size for size, is_dir in sizes.values() if is_dir and size <= THRESHOLD)


def main() -> None:
    input = sys.stdin.read().splitlines()
    print(solve(input))


if __name__ == "__main__":
    main()
