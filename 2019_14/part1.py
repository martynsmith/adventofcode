import typing
import fileinput
from collections import defaultdict
from decimal import Decimal, ROUND_CEILING
from pprint import pprint


class Component(typing.NamedTuple):
    quantity: int
    chemical: str


wanted = {}


def gimme(chemical, quantity):
    per_reaction_quantity = wanted[chemical]['you_get']
    ingredients = wanted[chemical]['you_need']

    requirements = {}

    repeats = (Decimal(quantity) / Decimal(per_reaction_quantity)).quantize(Decimal(1), rounding=ROUND_CEILING)

    for i in ingredients:  # type: Component
        requirements[i.chemical] = i.quantity * repeats

    return requirements


for line in fileinput.input():
    print(line.strip())
    i, o = line.strip().split(' => ')
    in_elements = []
    for block in i.split(', '):
        q, c = block.split(' ')
        in_elements.append(Component(int(q), c))
    if ',' in o:
        raise Exception("nope")
    q, c = o.split(' ')
    out_element = Component(int(q), c)

    wanted[out_element.chemical] = dict(
        you_get=out_element.quantity,  # how much you get
        you_need=tuple(in_elements),  # what you need
        depends_on=set(),
    )

print()

def calculate_deps(chemical):
    deps = set()
    for comp in wanted[chemical]['you_need']:
        if comp.chemical != 'ORE':
            deps.add(comp.chemical)
            deps.update(calculate_deps(comp.chemical))

    return deps


for chemical in wanted.keys():
    wanted[chemical]['depends_on'] = calculate_deps(chemical)


to_order = set(wanted.keys())
ordered_chemicals = []

while to_order:
    for c in to_order:
        if wanted[c]['depends_on'].issubset(set(ordered_chemicals)):
            ordered_chemicals.append(c)
            to_order.remove(c)
            break

# print(ordered_chemicals)


max_ore = 1000000000000

def ore_required(fuel):
    need = defaultdict(int)
    need['FUEL'] = fuel

    for chemical in reversed(ordered_chemicals):
        # print(f"need {need[chemical]} {chemical}")
        for c, q in gimme(chemical, need[chemical]).items():
            need[c] += q
        if chemical in need:
            del need[chemical]

    return need['ORE']

f = 11780000

while ore_required(f) < max_ore:
    print(f)
    f += 1

print()
print(ore_required(11788285))
print(ore_required(11788286))
print(ore_required(11788287))
print(max_ore)

# 460664 is too low
