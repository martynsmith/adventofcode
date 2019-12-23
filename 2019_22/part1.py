import fileinput

cards = list(range(10007))


def deal_with_increment(cards, inc):
    card_count = len(cards)
    new_cards = [None] * card_count
    i = 0
    while cards:
        new_cards[i] = cards.pop(0)
        i += inc
        i = i % card_count

    return new_cards


def cut(cards, pos):
    return cards[pos:] + cards[:pos]


for instruction in fileinput.input():  # type: str
    instruction = instruction.strip()

    if instruction.startswith('deal with increment '):
        cards = deal_with_increment(cards, int(instruction[20:]))
    elif instruction == 'deal into new stack':
        cards = list(reversed(cards))
    elif instruction.startswith('cut '):
        cards = cut(cards, int(instruction[4:]))
    else:
        raise NotImplementedError(instruction)

# print(" ".join([str(c) for c in cards]))
print(cards.index(2019))
