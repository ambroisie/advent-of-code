#!/usr/bin/env python

import itertools
import re
import sys
from typing import Dict, List


def parse_rule(raw_rules: List[str]) -> str:
    parsed: Dict[int, str] = {}
    rules = {int(num): rule.strip() for num, rule in (i.split(":") for i in raw_rules)}

    for n, r in rules.items():
        if '"' not in r:
            continue
        parsed[n] = r.replace('"', "")

    while 0 not in parsed:
        for num in parsed:
            if num not in rules:
                continue
            rules.pop(num)

        for num, r in rules.items():
            nums = list(reversed(sorted(map(int, re.findall("(\\d+)", r)))))
            if all(n in parsed for n in nums):
                for n in nums:
                    r = re.sub(str(n), parsed[n], r)  # Bigger numbers replaced first
                r = r.replace(" ", "")
                parsed[num] = "(" + r + ")"
    return parsed[0]


def solve(raw: List[str]) -> int:
    pattern = re.compile(parse_rule(list(itertools.takewhile(len, raw))))

    return sum(
        pattern.fullmatch(line) is not None for line in itertools.dropwhile(len, raw)
    )


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
