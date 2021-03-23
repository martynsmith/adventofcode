#!/usr/bin/env python

from collections import deque

initial_cups = [int(c) for c in "123487596"]
initial_cups = [int(c) for c in "389125467"]


def part1():
    cups = list(initial_cups)
    for move in range(1, 101):
        # print(f"-- move {move} --")
        # print(f"cups:", cups)
        pick_up = cups[1:4]
        # print(f"pick up:", pick_up)
        cups[1:4] = []
        destination = cups[0] - 1
        while destination not in cups:
            destination -= 1
            if destination <= 0:
                destination = 9
        # print("destination:", destination)
        destination_index = cups.index(destination) + 1
        cups[destination_index:destination_index] = pick_up
        cups.append(cups.pop(0))
        # print()

    # print("-- final --")
    index_of_one = cups.index(1)
    part1 = cups[index_of_one + 1:] + cups[:index_of_one]
    print("part1:", "".join(str(c) for c in part1))


def part2():
    cups = deque(initial_cups + list(range(6, 1000001)))
    # cups = deque(initial_cups)
    cups.rotate(-1)
    max_cup = max(cups)

    for move in range(1, 1001):
        # print(f"-- move {move} --")
        # print(f"cups:", cups)
        current_cup = cups[-1]
        pick_up = [
            cups.popleft(),
            cups.popleft(),
            cups.popleft(),
        ]

        # print(f"pick up:", pick_up)

        destination = current_cup - 1
        if destination == 0:
            destination = max_cup
        while destination in pick_up:
            destination -= 1
            if destination == 0:
                destination = max_cup
        destination_index = cups.index(destination)

        # TODO - handle error
        cups.insert(destination_index + 1, pick_up.pop())
        cups.insert(destination_index + 1, pick_up.pop())
        cups.insert(destination_index + 1, pick_up.pop())
        cups.rotate(-1)
        # print()

    # print("-- final --")
    index_of_one = cups.index(1)
    cups.rotate(-cups.index(1))
    cups.popleft()
    # print("part2:", "".join(str(c) for c in cups))
    # part1 = cups[index_of_one + 1:] + cups[:index_of_one]
    # print("part1:", "".join(str(c) for c in part1))


# part1()
part2()
