#!/usr/bin/env python

import json
import sys
from collections.abc import Iterator

JSONValue = int | str | list["JSONValue"] | dict[str, "JSONValue"]


def solve(input: str) -> int:
    def parse(input: str) -> JSONValue:
        return json.loads(input)

    def all_numbers(doc: JSONValue) -> Iterator[int]:
        if isinstance(doc, int):
            yield doc
        elif isinstance(doc, list):
            for it in doc:
                yield from all_numbers(it)
        elif isinstance(doc, dict):
            if "red" in doc.values():
                return
            for it in doc.values():
                yield from all_numbers(it)

    doc = parse(input)
    return sum(all_numbers(doc))


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
