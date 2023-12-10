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
DAY = 10


GOTO = [
    # {'-': (np.array([0, 1]), 0), '7': (np.array([]))}
]
# PIPES = {
#     '|': np.array([[-1,  0], [ 1,  0]]),
#     '-': np.array([[ 0, -1], [ 0,  1]]),
#     'L': np.array([[-1,  0], [ 0,  1]]),
#     'J': np.array([[-1,  0], [ 0, -1]]),
#     '7': np.array([[ 0, -1], [ 1,  0]]),
#     'F': np.array([[ 0,  1], [ 1,  0]]),
# }
PIPES = {
    '|': (3, 1),
    '-': (0, 2),
    'L': (3, 0),
    'J': (3, 2),
    '7': (1, 2),
    'F': (1, 0),
}
DIRECTIONS = [
    np.array([ 0,  1]),
    np.array([ 1,  0]),
    np.array([ 0, -1]),
    np.array([-1,  0]),
]


def _make_rules(pipes, dirs):
    walk_rules = [{}, {}, {}, {}]
    for p, (a, b) in pipes.items():
        walk_rules[(a + 2) % 4][p] = (b, dirs[b])
        walk_rules[(b + 2) % 4][p] = (a, dirs[a])
    return walk_rules
WALK_RULES = _make_rules(PIPES, DIRECTIONS)

# def bidi_walk(grid, start):
    # st
    # for i, d in DIRECTIONS:
        # test_pos = start + d

class Walker:

    def __init__(self, grid, pos, dir):
        self.grid = grid
        self.pos = pos
        self.dir = dir
        self.dist = 0
 
    def step(self):
        pipe = self.grid[tuple(self.pos)]
        self.dir, delta = WALK_RULES[self.dir][pipe]
        self.pos += delta
        self.dist += 1


def bidi_walk(grid):
    start = np.argwhere(grid == 'S')[0]
    walkers = []
    pos_lists = [[], []]
    for d, delta in enumerate(DIRECTIONS):
        print(tuple(start + delta))
        test_start = start + delta
        if np.all(test_start >= 0) and (test_pipe := grid[tuple(test_start)]) in PIPES:
            if test_pipe in WALK_RULES[d]:
                walkers.append(Walker(grid, test_start, d))
    while np.any(walkers[0].pos != walkers[1].pos):
        for w, pos_list in walkers:
            w.step()
    return walkers[0].dist + 1


def shoelace(xy):
    x = xy[0]
    y = xy[1]
    return 0.5 * (y * (np.roll(x, 1) - np.roll(x, -1)))


def main():
    data = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
    # print(WALK_RULES)
    data = aocd.get_data(day=DAY, year=YEAR)
    grid = np.array([list(l) for l in data.split('\n') if l])

    answer = bidi_walk(grid)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # answer = 
    # print(answer)
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
