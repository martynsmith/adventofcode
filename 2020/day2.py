#!/usr/bin/env python

import re

data = [re.search(r'(\d+)-(\d+) (\w): (\S+)', l.strip()).groups() for l in open('day2.txt').readlines()]

def part1():
    valid_count = 0
    for minimum, maximum, letter, password in data:
        if int(minimum) <= password.count(letter) <= int(maximum):
            valid_count += 1

    print(f"part1: {valid_count}")

def part2():
    valid_count = 0
    for minimum, maximum, letter, password in data:
        if (password[int(minimum) - 1] + password[int(maximum) - 1]).count(letter) == 1:
            valid_count += 1

    print(f"part2: {valid_count}")

part1()
part2()
