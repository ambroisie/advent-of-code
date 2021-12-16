#!/usr/bin/env python

import enum
import functools
import itertools
import math
import sys
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Iterator, List, Tuple, TypeVar

RawPacket = List[bool]


class PacketType(enum.IntEnum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITTERAL = 4
    GREATER = 5
    LESS = 6
    EQUAL = 7


class PacketLengthType(enum.IntEnum):
    TOTAL_BITS = 0  # Next 15 bits are the number of bits in the sub-packets
    TOTAL_PACKETS = 1  # Next 11 bits are the number of sub-packets


@dataclass
class PacketLength:
    type: PacketLengthType
    length: int


@dataclass
class Packet:
    version: int
    type: PacketType


@dataclass
class OperatorPacket(Packet):
    packets: List[Packet]


@dataclass
class LitteralPacket(Packet):
    number: int


def solve(input: List[str]) -> int:
    def to_raw(packet: str) -> RawPacket:
        def bits(n: int) -> Iterator[bool]:
            for i in range(3, -1, -1):
                yield bool(n & (1 << i))

        nums = [int(c, 16) for c in input[0]]
        return list(itertools.chain.from_iterable(bits(n) for n in nums))

    def bits_to_int(bits: Iterable[bool]) -> int:
        return functools.reduce(lambda a, b: (a << 1) + b, bits, 0)

    def parse_packet(p: RawPacket) -> Tuple[int, Packet]:
        def packet_version(p: RawPacket) -> int:
            return bits_to_int(p[:3])

        def packet_type(p: RawPacket) -> PacketType:
            return PacketType(bits_to_int(p[3:6]))

        def parse_length(p: RawPacket) -> Tuple[int, PacketLength]:
            assert packet_type(p) != PacketType.LITTERAL  # Sanity check
            type = PacketLengthType(bits_to_int(p[6:7]))
            if type == PacketLengthType.TOTAL_BITS:
                index = 7 + 15
                length = bits_to_int(p[7:index])
            else:
                index = 7 + 11
                length = bits_to_int(p[7:index])
            return index, PacketLength(type, length)

        def parse_litteral(p: RawPacket) -> Tuple[int, LitteralPacket]:
            version, type = packet_version(p), packet_type(p)
            assert type == PacketType.LITTERAL  # Sanity check
            index = 6
            bits: List[bool] = []
            while True:
                bits += p[index + 1 : index + 5]
                index += 5
                # Check if we were at the last one
                if p[index - 5] == 0:
                    break
            return index, LitteralPacket(version, type, bits_to_int(bits))

        def parse_operator(p: RawPacket) -> Tuple[int, OperatorPacket]:
            version, type = packet_version(p), packet_type(p)
            assert type != PacketType.LITTERAL  # Sanity check

            index, length = parse_length(p)
            packets: List[Packet] = []

            if length.type == PacketLengthType.TOTAL_BITS:
                sub_index = 0
                while sub_index < length.length:
                    parsed, packet = parse_packet(p[index:])
                    sub_index += parsed
                    index += parsed
                    packets.append(packet)
            else:
                while len(packets) < length.length:
                    parsed, packet = parse_packet(p[index:])
                    index += parsed
                    packets.append(packet)

            return index, OperatorPacket(version, type, packets)

        if packet_type(p) == PacketType.LITTERAL:
            return parse_litteral(p)
        return parse_operator(p)

    def eval(p: Packet) -> int:
        if p.type == PacketType.LITTERAL:
            assert isinstance(p, LitteralPacket)  # Sanity check
            return p.number
        assert isinstance(p, OperatorPacket)  # Sanity check

        packet_values = [eval(c) for c in p.packets]

        ops: Dict[PacketType, Callable[[List[int]], int]] = {
            PacketType.SUM: sum,
            PacketType.PRODUCT: math.prod,
            PacketType.MINIMUM: min,
            PacketType.MAXIMUM: max,
            PacketType.SUM: sum,
            PacketType.GREATER: lambda values: values[0] > values[1],
            PacketType.LESS: lambda values: values[0] < values[1],
            PacketType.EQUAL: lambda values: values[0] == values[1],
        }

        assert len(packet_values) >= 1  # Sanity check
        if p.type in (PacketType.GREATER, PacketType.LESS, PacketType.EQUAL):
            assert len(packet_values) == 2  # Sanity check

        return ops[p.type](packet_values)

    raw = to_raw(input[0])
    __, packet = parse_packet(raw)

    return eval(packet)


def main() -> None:
    input = [line.strip() for line in sys.stdin.readlines()]
    print(solve(input))


if __name__ == "__main__":
    main()
