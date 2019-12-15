from collections import defaultdict
import fileinput
from decimal import Decimal, ROUND_CEILING
import re

ingredients_for = {}
depends_on = {}
amount_produced = {}


# First we read all the data in
for line in fileinput.input():
    pairs = [(int(q), c) for q, c in re.compile(r'(\d+) (\w+)').findall(line)]
    out_quantity, out_chemical = pairs.pop(-1)
    amount_produced[out_chemical] = out_quantity
    ingredients_for[out_chemical] = pairs


# Figure out what chemicals depend on which
def calculate_deps(chemical):
    deps = set()
    for _, in_chemical in ingredients_for[chemical]:
        if in_chemical != 'ORE':
            deps.add(in_chemical)
            deps.update(calculate_deps(in_chemical))

    return deps


for chemical in amount_produced.keys():
    depends_on[chemical] = calculate_deps(chemical)

unordered_chemicals = set(amount_produced.keys())
ordered_chemicals = []

while unordered_chemicals:
    for chemical in unordered_chemicals:
        if depends_on[chemical].issubset(set(ordered_chemicals)):
            ordered_chemicals.insert(0, chemical)
            unordered_chemicals.remove(chemical)
            break


# Now for a given FUEL requirement we can determine the ORE requirement
def ore_required(fuel):
    need = defaultdict(int)
    need['FUEL'] = fuel

    for chemical in ordered_chemicals:
        for required_quantity, required_chemical in ingredients_for[chemical]:
            repeats = int((Decimal(need[chemical]) / Decimal(amount_produced[chemical])).quantize(Decimal(1), rounding=ROUND_CEILING))
            need[required_chemical] += required_quantity * repeats
        if chemical in need:
            del need[chemical]

    return need['ORE']

# Part 1
print(f"Part 1: {ore_required(1)} ORE required to produce 1 FUEL")

# Part 2 - binary search
target_ore = 1000000000000

min_fuel = 1
max_fuel = target_ore

while max_fuel - min_fuel > 1:
    new_fuel = min_fuel + (max_fuel - min_fuel) // 2
    if ore_required(new_fuel) < target_ore:
        min_fuel = new_fuel
    else:
        max_fuel = new_fuel

print(f"Part 2: {min_fuel} FUEL requires {ore_required(min_fuel)} ORE")
