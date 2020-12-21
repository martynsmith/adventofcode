#!/usr/bin/env python

from rich import print
import re

ingredient_for = {}

lines = open('day21.txt').readlines()
# lines = open('day21-sample.txt').readlines()

for line in lines:
    match = re.search(r'^(.*?)\(contains (.*?)\)$', line)
    ingredients = set(i.strip() for i in match.group(1).strip().split(' '))
    allergens = set(a.strip() for a in match.group(2).strip().split(','))

    for allergen in allergens:
        if allergen not in ingredient_for:
            ingredient_for[allergen] = ingredients
        else:
            ingredient_for[allergen] = ingredient_for[allergen].intersection(ingredients)

single_ingredients = set()
while set(len(i) for i in ingredient_for.values()) != {1}:
    for allergen, ingredients in ingredient_for.items():
        if len(ingredients) == 1:
            single_ingredients.update(ingredients)
        else:
            for si in single_ingredients:
                ingredients.discard(si)

for allergen, ingredients in ingredient_for.items():
    if len(ingredients) == 1:
        single_ingredients.update(ingredients)

part1 = 0
for line in lines:
    match = re.search(r'^(.*?)\(contains (.*?)\)$', line)
    ingredients = set(i.strip() for i in match.group(1).strip().split(' '))
    part1 += len(ingredients.difference(single_ingredients))

print("part1:", part1)
print("part2:", ",".join([i[1] for i in sorted([(a, list(i)[0]) for a, i in ingredient_for.items()])]))
