#!/usr/bin/env python3

import numpy as np
import aocd

YEAR = 2023
DAY = 10


PIPES = {
    '|': (1, 3),
    '-': (0, 2),
    'L': (3, 0),
    'J': (2, 3),
    '7': (1, 2),
    'F': (0, 1),
}
DIRS_TO_PIPE = {v: k for k, v in PIPES.items()}
DIRECTIONS = [
    np.array([ 0,  1]),
    np.array([ 1,  0]),
    np.array([ 0, -1]),
    np.array([-1,  0]),
]


def _make_rules(pipes, dirs):
    walk_rules = [{}, {}, {}, {}]
    for p, (a, b) in pipes.items():
        if np.all(dirs[a] + dirs[b] == 0):
            left = DIRECTIONS[(a + 1) % 4]
        else:
            left = dirs[a] + dirs[b]
        walk_rules[(a + 2) % 4][p] = (b, dirs[b], left)
        walk_rules[(b + 2) % 4][p] = (a, dirs[a], -left)
    return walk_rules
WALK_RULES = _make_rules(PIPES, DIRECTIONS)


class Walker:

    def __init__(self, grid, pos, d):
        self.grid = grid
        self.pos = pos
        self.dir = d
        self.dist = 0
        self.ltube = []
        self.rtube = []

    def step(self):
        pipe = self.grid[tuple(self.pos)]
        self.dir, delta, left = WALK_RULES[self.dir][pipe]
        self.ltube.append(self.pos + 0.5 * left)
        self.rtube.append(self.pos - 0.5 * left)
        self.pos += delta
        self.dist += 1


def bidi_walk(grid):
    start = np.argwhere(grid == 'S')[0]
    walkers = []
    for d, delta in enumerate(DIRECTIONS):
        test_start = start + delta
        if np.all(test_start >= 0) and (test_pipe := grid[tuple(test_start)]) in PIPES:
            if test_pipe in WALK_RULES[d]:
                walkers.append(Walker(grid, test_start, d))
    while np.any(walkers[0].pos != walkers[1].pos):
        for w in walkers:
            w.step()
    return walkers[0].dist + 1


def walk(grid):
    start = np.argwhere(grid == 'S')[0]
    start_dirs = []
    for d, delta in enumerate(DIRECTIONS):
        test_start = start + delta
        if np.all(test_start >= 0) and (test_pipe := grid[tuple(test_start)]) in PIPES:
            if test_pipe in WALK_RULES[d]:
                start_dirs.append(d)
    grid[tuple(start)] = DIRS_TO_PIPE[tuple(start_dirs)]
    walker = Walker(grid, np.copy(start), (start_dirs[0] + 2) % 4)
    walker.step()
    while np.any(walker.pos != start):
        walker.step()
    return np.column_stack(walker.ltube), np.column_stack(walker.rtube)


def shoelace(xy):
    x = xy[0]
    y = xy[1]
    return 0.5 * np.sum(y * (np.roll(x, 1) - np.roll(x, -1)))


def main():
    data = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
    data = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
    data = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    grid = np.array([list(l) for l in data.split('\n') if l])

    answer = bidi_walk(grid)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    lxy, rxy = walk(grid)
    answer = int(min(abs(shoelace(lxy)), abs(shoelace(rxy))))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
