from collections import defaultdict
import fileinput
import networkx
from decimal import Decimal, ROUND_CEILING
import re

ingredients_for = {}
amount_produced = {}
dep_tree = networkx.DiGraph()

# First we read all the data in
for line in fileinput.input():
    pairs = [(int(q), c) for q, c in re.compile(r'(\d+) (\w+)').findall(line)]
    out_quantity, out_chemical = pairs.pop(-1)
    amount_produced[out_chemical] = out_quantity
    ingredients_for[out_chemical] = pairs

    for _, c in pairs:
        dep_tree.add_edge(out_chemical, c)

# This is a list of chemicals such that chemicals only depend on those that
# come after them in the list
ordered_chemicals = list(networkx.topological_sort(dep_tree))
ordered_chemicals.remove('ORE')

print()
# from matplotlib import pyplot
# f = pyplot.figure()
# networkx.draw(dep_tree, with_labels=True, font_size=4)
# f.savefig('foo.pdf')


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
