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
DAY = 7

CARDS = 'AKQJT98765432'
CARD_VALUE = {c: i for i, c in enumerate(reversed(CARDS))}
JOKER_CARDS = 'AKQT98765432J'
JOKER_CARD_VALUE = {c: i for i, c in enumerate(reversed(JOKER_CARDS))}


@functools.total_ordering
class Hand:

    def __init__(self, cards):
        self.cards = cards

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.type == other.type:
            return self.values < other.values
        return self.type < other.type

    def __repr__(self):
        return f'Hand({self.cards})'

    @functools.cached_property
    def values(self):
        return tuple(CARD_VALUE[c] for c in self.cards)

    @functools.cached_property
    def type(self):
        counts = collections.Counter(self.cards)
        match len(counts):
            case 5:
                return 0
            case 4:
                return 1
            case 3:
                return counts.most_common(1)[0][1]
            case 2:
                return counts.most_common(1)[0][1] + 1
            case 1:
                return 6


@functools.total_ordering
class JokerHand(Hand):

    def __repr__(self):
        return f'JokerHand({self.cards})'

    @functools.cached_property
    def values(self):
        return tuple(JOKER_CARD_VALUE[c] for c in self.cards)

    @functools.cached_property
    def type(self):
        counts = collections.Counter(self.cards)
        if 'J' in counts:
            if counts['J'] == 5:
                return 6
            num_j = counts['J']
            counts['J'] = 0
            most_common_count = counts.most_common(1)[0][1] + num_j
            num_unique = len(counts) - 1
        else:
            most_common_count = counts.most_common(1)[0][1]
            num_unique = len(counts)
        match num_unique:
            case 5:
                return 0
            case 4:
                return 1
            case 3:
                return most_common_count
            case 2:
                return most_common_count + 1
            case 1:
                return 6


def main():
    test_cases = ['AAAAA', 'AA8AA', '23332', 'TTT98', '23432', 'A23A4', '23456']
    data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l.split() for l in data.split('\n') if l]
    deck = []
    for c, t in inlist:
        deck.append((Hand(c), int(t)))
    deck.sort()
    # [print(d) for d in deck]

    # for t in test_cases:
    #     print(t, Hand(t).type)
    answer = sum((i + 1) * b for i, (_, b) in enumerate(deck))
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    deck2 = []
    for c, t in inlist:
        deck2.append((JokerHand(c), int(t)))
    deck2.sort()
    [print(c, c.type, c.values) for c, _ in deck2]
    answer = sum((i + 1) * b for i, (_, b) in enumerate(deck2))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
