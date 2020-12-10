#!/usr/bin/env python

data = [int(l.strip()) for l in open('day01.txt').readlines()]

def part1():
    for x in data:
        for y in data:
            if x + y == 2020:
                print(f"part1: {x*y}")
                return


def part2():
    for x in data:
        for y in data:
            for z in data:
                if x + y + z == 2020:
                    print(f"part2: {x*y*z}")
                    return

part1()
part2()
