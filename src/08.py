#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import io
import itertools
import multiprocessing
import operator as op
import re
import timeit

import numpy as np
import aocd

import tulun

YEAR = 2023
DAY = 8


def parse_input(data_block):
    paths = {}
    for l in data_block.split('\n'):
        if not l:
            continue
        paths[l[:3]] = (l[7:10], l[12:15])
    return paths


def traverse(directions, paths, dest='ZZZ'):
    now = 'AAA'
    for i, d in enumerate(itertools.cycle(directions)):
        # print(d)
        now = paths[now][int(d == 'R')]
        # print(now)
        if now == dest:
            return i + 1


def parallel_traverse(directions, paths):
    now = set(d for d in paths.keys() if d[-1] == 'A')
    print(now)
    for i, d in enumerate(itertools.cycle(directions)):
        choice = int(d == 'R')
        now = set(paths[n][choice] for n in now)
        if all(n[-1] == 'Z' for n in now):
            print(now)
            return i + 1


def find_cycle(directions, paths, start):
    now = start
    for i, d in enumerate(itertools.cycle(directions)):
        now = paths[now][int(d == 'R')]
        if now[-1] == 'Z':
            return i + 1


# def find_cycles(directions, paths):
    # starts = set(d for d in paths.keys() if d[-1] == 'A')



def main():
    data = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
    data = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    dirs, data_block = data.split('\n\n')
    paths = parse_input(data_block)
    print(paths)

    # answer = traverse(dirs, paths)
    # print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    my_find_cycle = functools.partial(find_cycle, dirs, paths)
    starts = set(d for d in paths.keys() if d[-1] == 'A')
    cycles = list(map(my_find_cycle, starts))
    print(cycles)
    answer = np.lcm.reduce(cycles)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
