#!/usr/bin/env python3

import collections
import itertools

import numpy as np
import aocd

YEAR = 2023
DAY = 3


def parse_grid(grid):
    num_coords = {}
    symb_coords = {}
    for i, row in enumerate(grid):
        in_num = False
        pos = []
        buffer = []
        for j, c in enumerate(row):
            match c:
                case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                    if not in_num:
                        pos.append(i)
                        pos.append(j)
                        in_num = True
                    buffer.append(c)
                    continue
                case '.':
                    pass
                case _:
                    symb_coords[(i, j)] = c
            if in_num:
                in_num = False
                pos.append(j)
                num_coords[tuple(pos)] = int(''.join(buffer))
                pos.clear()
                buffer.clear()
        # End-of-line edge case. Ouch!
        if in_num:
            pos.append(len(row))
            num_coords[tuple(pos)] = int(''.join(buffer))
    return num_coords, symb_coords


def is_adj_symb(pos, symb_coords):
    i, j0, j1 = pos
    for di, j in itertools.product([-1, 1], range(j0-1, j1+1)):
        if (i + di, j) in symb_coords:
            return True
    for j in [j0 - 1, j1]:
        if (i, j) in symb_coords:
            return True
    return False


def find_adj_gear(pos, symb_coords):
    i, j0, j1 = pos
    adj_symbs = []
    for di, j in itertools.product([-1, 1], range(j0-1, j1+1)):
        if (symb_pos := (i + di, j)) in symb_coords:
            if symb_coords[symb_pos] == '*':
                adj_symbs.append(symb_pos)
    for j in [j0 - 1, j1]:
        if (symb_pos := (i, j)) in symb_coords:
            if symb_coords[symb_pos] == '*':
                adj_symbs.append(symb_pos)
    return adj_symbs


def list_num_adj_symb(num_coords, symb_coords):
    num_list = []
    for pos, v in num_coords.items():
        if is_adj_symb(pos, symb_coords):
            num_list.append(v)
    return num_list


def list_num_adj_gear(num_coords, symb_coords):
    gear_dict = collections.defaultdict(list)
    for pos, v in num_coords.items():
        if gear_list := find_adj_gear(pos, symb_coords):
            for g in gear_list:
                gear_dict[g].append(v)
    return gear_dict


def main():
    data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    data = aocd.get_data(day=DAY, year=YEAR)
    grid = [list(l) for l in data.split('\n') if l]

    num_c, sym_c = parse_grid(grid)
    answer = sum(list_num_adj_symb(num_c, sym_c))
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(np.prod(x) for x in list_num_adj_gear(num_c, sym_c).values() if len(x) == 2)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
