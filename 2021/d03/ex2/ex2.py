#!/usr/bin/env python

import sys
from copy import deepcopy
from typing import List


def solve(input: List[int]) -> int:
    def highest_pow2(n: int) -> int:
        return len(bin(n)) - 2 - 1  # '0b' prefix, and off-by-one

    def count_bits_at(input: List[int], bit: int) -> int:
        return sum((n & pow(2, bit)) != 0 for n in input)

    def filter_by_bit_value(input: List[int], bit: int, value: int) -> List[int]:
        # Simplify the filter by mapping the value to the actual power of 2
        if value != 0:
            value = pow(2, bit)
        return list(filter(lambda n: (n & pow(2, bit)) == value, input))

    def filter_oxygen(input: List[int], bit: int) -> List[int]:
        # No further processing needed
        if len(input) <= 1:
            return input

        num_bits = count_bits_at(input, bit)
        # Keep 1s on equality
        if num_bits >= len(input) / 2:
            return filter_by_bit_value(input, bit, 1)
        else:
            return filter_by_bit_value(input, bit, 0)

    def filter_co2(input: List[int], bit: int) -> List[int]:
        # No further processing needed
        if len(input) <= 1:
            return input

        num_bits = count_bits_at(input, bit)
        # Keep 0s on equality
        if num_bits < len(input) / 2:
            return filter_by_bit_value(input, bit, 1)
        else:
            return filter_by_bit_value(input, bit, 0)

    oxygen, co2 = 0, 0
    max_bit = max(highest_pow2(n) for n in input)
    oxygen_input, co2_input = deepcopy(input), deepcopy(input)

    for bit in range(max_bit, -1, -1):
        oxygen_input = filter_oxygen(oxygen_input, bit)
        co2_input = filter_co2(co2_input, bit)

        if len(oxygen_input) == 1:
            oxygen = oxygen_input[0]
        if len(co2_input) == 1:
            co2 = co2_input[0]

    return oxygen * co2


def main() -> None:
    input = [int(line, 2) for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
