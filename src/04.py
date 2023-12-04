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
DAY = 4


def parse_card(line):
    _, nums = line.split(': ')
    winning, haves = nums.split(' | ')
    return set(map(int, winning.split())), list(map(int, haves.split()))


def count_winning(winning, nums):
    score = 0
    for x in nums:
        if x in winning:
            if score == 0:
                score = 1
            else:
                score *= 2
    return score


def count_winning2(winning, nums):
    score = 0
    for x in nums:
        if x in winning:
            score += 1
    return score


def tally_copies(cards):
    copies = []
    num_cards = len(cards)
    for i, (winning, nums) in enumerate(cards):
        wins = count_winning2(winning, nums)
        copies.append(list(range(i+1, min(i+1+wins, num_cards))))
    return copies


def count_copies(cards):
    num_cards = len(cards)
    counts = np.ones(num_cards, dtype=np.int64)
    for i, c in enumerate(cards):
        for j in c:
            counts[j] += counts[i]
    return counts


def make_count_copies(copies):
    @functools.cache
    def count_copies(i):
        count = 1
        for c in copies[i]:
            count += count_copies(c)
        return count




def main():
    data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    cards = [parse_card(l) for l in data.split('\n') if l]
    print(cards)

    answer = sum(count_winning(*c) for c in cards)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    tallies = tally_copies(cards)
    counts = count_copies(tallies)
    print(counts)
    answer = np.sum(counts)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
