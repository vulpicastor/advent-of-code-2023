#!/usr/bin/env python3

import collections

import aocd

YEAR = 2023
DAY = 15


def ahash(s):
    out = 0
    for c in s:
        out += ord(c)
        out *= 17
        out %= 256
    return out


class HashMap:

    def __init__(self):
        self.buckets = []
        for _ in range(256):
            self.buckets.append(collections.deque())

    def __repr__(self):
        return repr({i: b for i, b in enumerate(self.buckets) if b})

    def __delitem__(self, key):
        h = ahash(key)
        bucket = self.buckets[h]
        for i in range(len(bucket)):  # pylint: disable=consider-using-enumerate
            if bucket[i][0] == key:
                bucket.rotate(-i)
                bucket.popleft()
                bucket.rotate(i)
                return

    def __setitem__(self, key, value):
        h = ahash(key)
        bucket = self.buckets[h]
        for i in range(len(bucket)):  # pylint: disable=consider-using-enumerate
            if bucket[i][0] == key:
                bucket.rotate(-i)
                bucket.popleft()
                bucket.appendleft((key, value))
                bucket.rotate(i)
                return
        bucket.append((key, value))

    def update(self, inst):
        if inst[-1] == '-':
            del self[inst[:-1]]
        else:
            key, val = inst.split('=')
            self[key] = int(val)

    def power(self):
        out = 0
        for i, b in enumerate(self.buckets):
            for j, (_, v) in enumerate(b):
                out += (i + 1) * (j + 1) * v
        return out


def main():
    data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l for l in data.split(',')]

    print(list(ahash(s) for s in inlist))
    answer = sum(ahash(s) for s in inlist)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    hashmap = HashMap()
    for s in inlist:
        hashmap.update(s)
    answer = hashmap.power()
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
