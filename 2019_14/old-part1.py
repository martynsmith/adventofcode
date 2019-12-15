import typing
import fileinput
from pprint import pprint


class Component(typing.NamedTuple):
    quantity: int
    chemical: str


wanted = {}


def gimme(chemical, quantity):
    per_reaction_quantity, ingredients = wanted[chemical]

    requirements = {}

    while quantity > 0:
        for i in ingredients:  # type: Component
            requirements.setdefault(i.chemical, 0)
            requirements[i.chemical] += i.quantity
        quantity -= per_reaction_quantity

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

pprint(wanted)
