#!/usr/bin/env python

from rich import print
import re

rules, messages = open('day19.txt').read().strip().split('\n\n')
rules = dict(r.split(': ') for r in rules.strip().split('\n'))
messages = messages.strip().split('\n')

rule0 = rules['0']
while re.search(r'\d', rule0):
    rule0 = re.sub(r'(\d+)', lambda m: "(" + rules[m.group(1)] + ")", rule0)

rule0 = re.sub(r'\("(\w)"\)', r'\1', rule0)
rule0 = re.sub(r'\s+', r'', rule0)
rule0 = f"^{rule0}$"

count = 0
for message in messages:
    if re.search(rule0, message):
        count += 1

print("part1:", count)

rule0 = rules['0']
rules['8'] = '42+'
# This is really evil and hacky
rules['11'] = '42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31'

while re.search(r'\d', rule0):
    rule0 = re.sub(r'(\d+)', lambda m: "(" + rules[m.group(1)] + ")", rule0)

rule0 = re.sub(r'\("(\w)"\)', r'\1', rule0)
rule0 = re.sub(r' +', r'', rule0)
rule0 = f"^{rule0}$"

count = 0
for message in messages:
    if re.search(rule0, message):
        count += 1

print("part2:", count)
