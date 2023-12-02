#!/usr/bin/env python3

import re

import aocd

YEAR = 2023
DAY = 1


def cal_val(s):
    for c in s:
        if c.isnumeric():
            first = c
            break
    for c in s[::-1]:
        if c.isnumeric():
            last = c
            break
    return int(first + last)


english = {w: i+1 for i, w in enumerate('one two three four five six seven eight nine'.split())}


def cal_val_2(s):
    # Shamelessly borrowed from https://stackoverflow.com/questions/5616822/how-to-use-regex-to-find-all-overlapping-matches.
    m = re.findall(r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))', s)
    digits = []
    for d in m:
        match d:
            case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                digits.append(int(d))
            case _:
                digits.append(english[d])
    return digits[0] * 10 + digits[-1]


def main():
    data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
    data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l for l in data.split('\n') if l]

    answer = sum(cal_val(s) for s in inlist)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sum(cal_val_2(s) for s in inlist)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
