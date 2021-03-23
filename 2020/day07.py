#!/usr/bin/env python

from dataclasses import dataclass
from typing import List, Dict
from rich import print
import re


@dataclass
class Bag:
    bag: str
    deps: 'List[Dep]'

    def contains(self, check: 'Bag'):
        if len([x for x in self.deps if x.bag == check]):
            return True

        for dep in self.deps:
            if dep.bag.contains(check):
                return True

        return False

    def count_subbags(self) -> int:
        count = 0
        for dep in self.deps:
            count += dep.number
            count += dep.number * dep.bag.count_subbags()

        return count


@dataclass
class Dep:
    number: int
    bag: Bag


bag_by_name: Dict[str, Bag] = {}

data = open('day07.txt').readlines()

for line in data:
    match = re.search(r'^(.*?) bags contain (.*)\.$', line)
    if not match:
        raise Exception(f"nope: {line}")
    bag_name = match.group(1)
    try:
        deps = [re.search(r'^(\d+) (.*?) bags?$', m).groups() for m in match.group(2).split(', ')]
    except:
        deps = []

    bag_by_name.setdefault(bag_name, Bag(bag=bag_name, deps=[]))
    bag = bag_by_name[bag_name]
    for dep_count, dep_name in deps:
        bag_by_name.setdefault(dep_name, Bag(bag=bag_name, deps=[]))
        bag.deps.append(Dep(number=int(dep_count), bag=bag_by_name[dep_name]))

print(f"part1: {len([b for b in bag_by_name.values() if b.contains(bag_by_name['shiny gold'])])}")
print(f"part2: {bag_by_name['shiny gold'].count_subbags()}")
