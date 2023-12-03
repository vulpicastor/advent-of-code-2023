#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import aocd

YEAR = 2023
DAY = 3


def is_empty(a):
    return a == '.'


def is_num(a):
    mask = np.zeros_like(a, dtype=bool)
    for i in range(10):
        mask |= a == str(i)
    return mask


def num_adj_symbol(a):
    nrow, ncol = a.shape
    mask = np.zeros((nrow+2, ncol+2), dtype=bool)
    empty_mask = is_empty(a)
    num_mask = is_num(a)
    symbol_mask = np.logical_not(empty_mask | num_mask)
    for di, dj in itertools.product([-1, 0, 1], [-1, 0, 1]):
        mask[1+di:nrow+1+di, 1+dj:ncol+1+dj] |= symbol_mask
    mask[1:-1, 1:-1] &= num_mask
    return mask[1:-1, 1:-1]


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
            pos.append(j+1)
            num_coords[tuple(pos)] = int(''.join(buffer))
    return num_coords, symb_coords


def is_adj_symb(pos, symb_coords, v):
    i, j0, j1 = pos
    for di, j in itertools.product([-1, 1], range(j0-1, j1+1)):
        if (i + di, j) in symb_coords:
            # print('Good', pos, v, symb_coords[(i + di, j)])
            return True
    for j in [j0 - 1, j1]:
        if (i, j) in symb_coords:
            # print('Good', pos, v, symb_coords[(i, j)])
            return True
    return False


def find_adj_gear(pos, symb_coords, v):
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
        if is_adj_symb(pos, symb_coords, v):
            num_list.append(v)
    return num_list

def list_num_adj_gear(num_coords, symb_coords):
    gear_dict = collections.defaultdict(list)
    for pos, v in num_coords.items():
        if gear_list := find_adj_gear(pos, symb_coords, v):
            print(gear_list)
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
    inlist = [list(l) for l in data.split('\n') if l]
    # print(inlist)
    grid = np.array(inlist)
    print(grid)

    num_c, sym_c = parse_grid(grid)
    print(num_c)
    print(sym_c)
    # print(list_num_adj_symb(num_c, sym_c))
    answer = sum(list_num_adj_symb(num_c, sym_c))
    # print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(np.prod(x) for x in list_num_adj_gear(num_c, sym_c).values() if len(x) == 2)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
