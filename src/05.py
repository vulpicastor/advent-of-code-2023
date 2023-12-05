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
import sortedcontainers
import aocd

YEAR = 2023
DAY = 5


def page_table_key(x):
    return x[1]


def parse_mapping(data_block):
    lines = data_block.split('\n')
    src_key, _, dest_key = lines[0].split()[0].split('-')
    page_table = sortedcontainers.SortedKeyList(key=page_table_key)
    for l in lines[1:]:
        if l:
            page_table.add(tuple(map(int, l.split())))
    return src_key, dest_key, page_table


def parse_input(data):
    data_blocks = data.split('\n\n')
    seeds = list(map(int, data_blocks[0].split(': ')[1].split()))
    mappings = {}
    key_mapping = {}
    dest_key = ''
    for d in data_blocks[1:]:
        src_key, dest_key, page_table = parse_mapping(d)
        mappings[src_key] = page_table
        key_mapping[src_key] = dest_key
    key_mapping[dest_key] = None
    return seeds, mappings, key_mapping


def translate(addr, page_table):
    entry_i = page_table.bisect_key_right(addr) - 1
    # print(addr, entry_i, page_table[entry_i])
    if entry_i < 0:
        return addr
    dest_begin, src_begin, map_size = page_table[entry_i]
    if addr < src_begin + map_size:
        return dest_begin + (addr - src_begin)
    return addr


def walk_page_tables(addr, mappings, key_mappings):
    key = 'seed'
    map_seq = [addr]
    while key in mappings:
        page_table = mappings[key]
        addr = translate(addr, page_table)
        map_seq.append(addr)
        key = key_mappings[key]
    # print(map_seq)
    return addr


def range_translate(addr, size, page_table):
    page_table_size = len(page_table)
    begin_i = page_table.bisect_key_right(addr) - 1
    mapped_ranges = []
    # Edge case: [addr (next_src_begin, xx), ...].
    if begin_i < 0:
        _, next_src_begin, _ = page_table[0]
        # Edge case: [(addr, size), (next_src_begin, xx), ...].
        if addr + size <= next_src_begin:
            return [(addr, size)]  # Unmapped.
        # else, size > (consumed_size := next_src_begin - addr).
        consumed_size = next_src_begin - addr
        mapped_ranges.append((addr, consumed_size))  # Unmapped.
        # Advance state to the start of next mapped range.
        addr = next_src_begin
        size -= consumed_size  # Guaranteed > 0.
        begin_i = 0
    dest_begin, src_begin, map_size = page_table[begin_i]
    # Edge case: [..., (src_begin, map_size), addr <-unmapped size-> (next_src_begin, xx), ...]
    if addr >= src_begin + map_size:
        # Edge case: We're beyond the end of the last mapped range.
        if begin_i + 1 >= page_table_size:
            mapped_ranges.append((addr, size))
            return mapped_ranges
        _, next_src_begin, _ = page_table[begin_i + 1]
        unmapped_size = next_src_begin - addr
        # Gap to next_src_begin completely consumes the remaining size.
        if unmapped_size >= size:
            mapped_ranges.append((addr, size))  # Unmapped.
            return mapped_ranges
        mapped_ranges.append((addr, unmapped_size))  # Unmapped.
        # Advance state to the start of next mapped range.
        addr = next_src_begin
        size -= unmapped_size # Guaranteed > 0.
        begin_i += 1
    # At this point, [..., (src_begin, addr src_end), (xx, xx), ...],
    # i.e. src_begin <= addr < src_begin + map_size.
    for i in range(begin_i, page_table_size):
        dest_begin, src_begin, map_size = page_table[i]
        src_end = src_begin + map_size  # Exclusive.
        map_begin = dest_begin + (addr - src_begin)
        consumed_size = src_end - addr
        # Current mapped range consumes the remainder.
        if consumed_size >= size:
            mapped_ranges.append((map_begin, size))  # Mapped.
            return mapped_ranges
        # Drat, we have stuff left.
        mapped_ranges.append((map_begin, consumed_size))  # Mapped.
        # Advance state beyond the end of the current range.
        addr = src_end
        size -= consumed_size
        # Edge case: We're beyond the end of the last mapped range.
        if i + 1 >= page_table_size:
            mapped_ranges.append((addr, size))
            return mapped_ranges
        _, next_src_begin, _ = page_table[i + 1]
        # If there is no gap until next range, continue.
        if src_end >= next_src_begin:
            continue
        unmapped_size = next_src_begin - addr
        # Gap to next_src_begin completely consumes the remaining size.
        if unmapped_size >= size:
            mapped_ranges.append((addr, size))  # Unmapped.
            return mapped_ranges
        mapped_ranges.append((addr, unmapped_size))  # Unmapped
        # Advance state to the start of next mapped range.
        addr = next_src_begin
        size -= unmapped_size # Guaranteed > 0.
    # mapped_ranges.sort()
    return mapped_ranges


def range_walk_page_tables(ranges, mappings, key_mappings):
    key = 'seed'
    map_seq = [ranges]
    while key in mappings:
        page_table = mappings[key]
        new_ranges = []
        for addr, size in ranges:
            new_ranges.extend(range_translate(addr, size, page_table))
        map_seq.append(new_ranges)
        ranges = new_ranges
        key = key_mappings[key]
    print(map_seq)
    return ranges


def merge_sorted_ranges(ranges):
    pass
    new_ranges = []
    old_begin = 0  # Inclusive.
    old_end = 0  # Exclusive.
    for begin, size in ranges:
        if begin < old_end:
            old_end = begin + size
            continue
        new_ranges.append((old_begin, old_end - old_begin))
        old_begin = begin
        old_end = begin + size


def main():
    data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    seeds, mapping, key_mapping = parse_input(data)
    # print(seeds)
    # print(mapping)
    # print(key_mapping)

    answer = min(walk_page_tables(s, mapping, key_mapping) for s in seeds)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    seed_ranges = list(itertools.batched(seeds, n=2))
    print(range_walk_page_tables(seed_ranges, mapping, key_mapping))
    answer = min(x[0] for x in range_walk_page_tables(seed_ranges, mapping, key_mapping))
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
