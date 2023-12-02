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
DAY = 2


def parse_input_line(line):
    game, trials = line.split(': ')
    game_num = int(game[5:])
    trial_list = []
    for t in trials.split('; '):
        print(t)
        new_trial = {}
        for i in t.split(', '):
            print(i)
            n, color = i.split()
            new_trial[color] = int(n)
        trial_list.append(new_trial)
    return game_num, trial_list


def is_game_possible(trial_list, bag_content):
    for t in trial_list:
        for color, n in bag_content.items():
            if color not in t:
                continue
            if t[color] > n:
                return False
    return True


def fewest_bag(trial_list):
    bag = {}
    for t in trial_list:
        for color, n in t.items():
            if color not in bag:
                bag[color] = n
            else:
                if n > bag[color]:
                    bag[color] = n
    return bag


def main():
    data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l for l in data.split('\n') if l]
    games = {}
    for l in inlist:
        k, v = parse_input_line(l)
        games[k] = v

    bag_content = {'red': 12, 'green': 13, 'blue': 14}
    answer = sum(game_id for game_id, trial_list in games.items() if is_game_possible(trial_list, bag_content))
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(functools.reduce(op.mul, fewest_bag(g).values()) for g in games.values())
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
