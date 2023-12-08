#!/usr/bin/env python3

import functools
import itertools

import numpy as np
import aocd

YEAR = 2023
DAY = 8


def traverse(directions, paths, start='AAA', stop_func=lambda s: s=='ZZZ'):
    now = start
    for i, d in enumerate(itertools.cycle(directions)):
        now = paths[now][int(d == 'R')]
        if stop_func(now):
            return i + 1


def parallel_traverse(directions, paths):
    my_find_cycle = functools.partial(
        traverse, directions, paths, stop_func=lambda s: s[-1]=='Z')
    starts = set(d for d in paths.keys() if d[-1] == 'A')
    return np.lcm.reduce(list(map(my_find_cycle, starts)))


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

AAA = (11B, XXX)
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
    paths = {l[:3]: (l[7:10], l[12:15]) for l in data_block.split('\n') if l}

    answer = traverse(dirs, paths)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = parallel_traverse(dirs, paths)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
