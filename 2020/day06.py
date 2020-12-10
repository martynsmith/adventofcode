#!/usr/bin/env python

import re

data = open('day6.txt').read()
groups = re.split(r'\n\n+', data.strip())

yes_count = 0
for group in groups:
    answers = set(re.sub(r'\s+', '', group))
    yes_count += len(answers)

print(f"part1: {yes_count}")

yes_count = 0
for group in groups:
    answers = re.split(r'\n', group)
    yes = set(answers.pop(0))
    for answer in answers:
        yes = yes.intersection(set(answer))

    yes_count += len(yes)

print(f"part2: {yes_count}")
