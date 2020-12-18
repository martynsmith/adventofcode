#!/usr/bin/env python

from rich import print
import re

data = [l.strip() for l in open('day18.txt').readlines()]


# data = [
#     "1 + 2 * 3 + 4 * 5 + 6"
# ]


class WeirdMath:
    def __init__(self, n):
        self.n = n

    def __add__(self, other):
        return WeirdMath(self.n + other.n)

    def __sub__(self, other):
        return WeirdMath(self.n * other.n)


total = 0
for row in data:
    row = re.sub(r'(\d+)', 'WeirdMath(\\1)', row)
    row = re.sub(r'\*', '-', row)
    total += eval(row).n

print("part1:", total)


class WeirdMath2:
    def __init__(self, n):
        self.n = n

    def __sub__(self, other):
        return WeirdMath2(self.n * other.n)

    def __mul__(self, other):
        return WeirdMath2(self.n + other.n)


total = 0
for row in data:
    row = re.sub(r'(\d+)', 'WeirdMath2(\\1)', row)
    row = re.sub(r'\*', '-', row)
    row = re.sub(r'\+', '*', row)
    total += eval(row).n

print("part2:", total)
