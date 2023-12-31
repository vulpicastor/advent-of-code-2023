#!/usr/bin/env python3

import numpy as np
import aocd

YEAR = 2023
DAY = 9


def diff_extrap(a):
    last = []
    while np.any(a):
        last.append(a[-1])
        a = np.diff(a)
    return sum(last)


def diff_extrap_left(a):
    first = []
    while np.any(a):
        first.append(a[0])
        a = np.diff(a)
    x = first.pop()
    while first:
        x = first.pop() - x
    return x


def main():
    data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [list(map(int, l.split())) for l in data.split('\n') if l]

    answer = sum(diff_extrap(a) for a in inlist)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(diff_extrap_left(a) for a in inlist)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
