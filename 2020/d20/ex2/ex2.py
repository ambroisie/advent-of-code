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
        tile = [
            [tile[j][i] for j in range(len(tile))]
            for i in range(len(tile[0]) - 1, -1, -1)
        ]
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


def trim(trans: Transforms, tiling: Tiling) -> Tile:
    def trim_tile(tile: Tile) -> Tile:
        return [line[1:-1] for line in tile[1:-1]]

    def tiling_to_tile(tiling: List[List[Tile]]) -> Tile:
        res: Tile = []
        for i in range(len(tiling) * len(tiling[0][0])):
            res.append([])
            tile_line_idx = i % len(tiling[0][0])
            for j in range(len(tiling[0]) * len(tiling[0][0][0])):
                tile = tiling[i // len(tiling[0][0])][j // len(tiling[0][0][0])]
                tile_row_idx = j % len(tiling[0][0][0])
                res[-1].append(tile[tile_line_idx][tile_row_idx])
        return res

    tiles = [[trim_tile(trans[num][id]) for num, id in line] for line in tiling]
    return tiling_to_tile(tiles)


def find_monster(image: Tile, monster: Tile) -> Iterator[Tuple[int, int]]:
    def monster_at(x: int, y: int) -> bool:
        for i in range(len(monster)):
            for j in range(len(monster[0])):
                if monster[i][j] == " ":
                    continue
                if image[x + i][y + j] != "#":
                    return False
        return True

    # Returns upper left corner if found
    for i in range(len(image) - len(monster)):
        for j in range(len(image[0]) - len(monster[0])):
            if monster_at(i, j):
                yield i, j


def remove_monster(image: Tile, monster: Tile, x: int, y: int) -> None:
    for i in range(len(monster)):
        for j in range(len(monster[0])):
            if monster[i][j] == " ":
                continue
            image[x + i][y + j] = " "


def solve(tiles: Tiles) -> int:
    image = trim(*build_tiling(tiles))
    monster = [
        [char for char in line]
        for line in (
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   ",
        )
    ]
    monsters = transforms(monster)

    for monster in monsters:
        for coords in find_monster(image, monster):
            remove_monster(image, monster, *coords)

    return sum(sum(char == "#" for char in line) for line in image)


def main() -> None:
    input = parse(sys.stdin.read())
    print(solve(input))


if __name__ == "__main__":
    main()
