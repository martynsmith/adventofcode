#!/usr/bin/env python

data = [6, 13, 1, 15, 2, 0]


def run(count):
    i = 1
    index_of = {}
    last = None
    index_setter = None

    for i, n in enumerate(data):
        index_of[n] = i + 1

    i += 1
    while i <= count:
        if last in index_of:
            n = i - index_of[last] - 1
        else:
            n = 0

        last = n
        if index_setter:
            index_of[index_setter[0]] = index_setter[1]

        index_setter = (n, i)
        i += 1

    return n


print(f"part1: {run(2020)}")
print(f"part2: {run(30000000)}")
