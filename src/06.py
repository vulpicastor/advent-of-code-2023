#!/usr/bin/env python3

import numpy as np
import aocd

YEAR = 2023
DAY = 6


def count_wins(t, d):
    P = t / 2
    D = np.sqrt(P*P -d)
    # Lol I'm sure there's a better way to find "the integer strictly less
    # than this number".
    max_t = P + D
    max_t -= 1 * (np.floor(max_t) == max_t)
    min_t = P - D
    min_t += 1 * (np.ceil(min_t) == min_t)
    return np.floor(max_t) - np.ceil(min_t) + 1


def main():
    data = """Time:      7  15   30
Distance:  9  40  200
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    times, dists = [np.array(list(map(int, l.split(':')[1].split()))) for l in data.split('\n') if l]

    answer = int(np.prod(count_wins(times, dists)))
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    lt, ld = [int(''.join(l.split(':')[1].split())) for l in data.split('\n') if l]
    answer = int(count_wins(lt, ld))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
