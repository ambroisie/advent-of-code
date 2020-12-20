#!/usr/bin/env python

import functools
import itertools
import math
import sys
from collections import defaultdict
from copy import deepcopy
from typing import Dict, Iterator, List, Set, Tuple

Tile = List[List[str]]
Tiles = Dict[int, Tile]


def parse(raw: str) -> Tiles:
    def parse_tile(raw: List[str]) -> Tile:
        return [[line[i] for i in range(len(line))] for line in raw]

    res = {}
    for lines in map(lambda s: s.splitlines(), raw.split("\n\n")):
        if len(lines) == 0:
            continue
        nums = int(lines[0][5:-1])
        res[nums] = parse_tile(lines[1:])
    return res


def rotations(tile: Tile) -> Iterator[Tile]:
    yield tile
    for __ in range(3):
        prev = deepcopy(tile)
        for i in range(len(tile)):
            for j in range(len(tile[i])):
                prev[i][j] = tile[len(tile) - j - 1][i]
        tile = prev
        yield tile


def flips(tile: Tile) -> Iterator[Tile]:
    yield tile
    yield tile[::-1]
    yield [line[::-1] for line in tile]
    yield [line[::-1] for line in tile[::-1]]


def transforms(tile: Tile) -> List[Tile]:
    # Can't use a set with lists...
    res: List[Tile] = functools.reduce(
        lambda l, it: l + [it] if not any(it == other for other in l) else l,
        itertools.chain.from_iterable(map(rotations, flips(tile))),
        [],
    )
    return res


def borders(tile: Tile) -> Iterator[str]:
    # They should match on same axis (i.e: go clockwise and counter-clockwise)
    return map(
        lambda s: "".join(s),
        [
            tile[0],
            [line[-1] for line in tile],
            tile[-1],
            [line[0] for line in tile],
        ],
    )


Transforms = Dict[int, List[Tile]]
Tiling = List[List[Tuple[int, int]]]  # Which tile, and which transform


def build_tiling(tiles: Tiles) -> Tuple[Transforms, Tiling]:
    transform_mapping = {num: transforms(tile) for num, tile in tiles.items()}
    trans_borders: Dict[int, Dict[int, List[str]]] = defaultdict(dict)
    for num, trans in transform_mapping.items():
        for i, t in enumerate(trans):
            trans_borders[num][i] = list(borders(t))
    length = math.isqrt(len(tiles))
    tiling = [[(-1, -1)] * length for __ in range(length)]

    def rec(x: int = 0, y: int = 0, used: Set[int] = set()) -> bool:
        if x == length:
            return True
        for num, borders in trans_borders.items():
            if num in used:
                continue
            used |= {num}

            for trans, border in borders.items():
                top, __, __, left = border
                if y > 0:
                    nid, ntrans = tiling[x][y - 1]
                    __, right, __, __ = trans_borders[nid][ntrans]
                    if left != right:
                        continue
                if x > 0:
                    nid, ntrans = tiling[x - 1][y]
                    __, __, bottom, __ = trans_borders[nid][ntrans]
                    if top != bottom:
                        continue
                tiling[x][y] = num, trans

                next_x, next_y = (x, y + 1) if y < (length - 1) else (x + 1, 0)
                if rec(next_x, next_y, used):
                    return True

            used -= {num}

        tiling[x][y] = (-1, -1)
        return False

    assert rec()
    return transform_mapping, tiling


def solve(tiles: Tiles) -> int:
    transforms, tiling = build_tiling(tiles)
    return tiling[0][0][0] * tiling[0][-1][0] * tiling[-1][0][0] * tiling[-1][-1][0]


def main() -> None:
    input = parse(sys.stdin.read())
    print(solve(input))


if __name__ == "__main__":
    main()
