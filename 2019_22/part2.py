import fileinput

deck_size = 119315717514047
shuffle_count = 101741582076661
initial_card_position = 2020


# deck_size = 10
# shuffle_count = 1
# initial_card_position = 2

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def deal_with_increment_factory(inc):
    mi = modinv(inc, deck_size)

    def inner(card_pos):
        return mi * card_pos % deck_size

    return inner


def reverse(card_pos):
    return deck_size - 1 - card_pos


def cut_factory(init_cut_pos):
    def inner(card_pos):
        if init_cut_pos >= 0:
            cut_pos = deck_size - init_cut_pos
        else:
            cut_pos = -init_cut_pos

        if card_pos < cut_pos:
            return deck_size - cut_pos + card_pos
        else:
            return card_pos - cut_pos

    return inner


def parse_instruction(instruction):
    instruction = instruction.strip()
    # print(instruction)

    if instruction.startswith('deal with increment '):
        return deal_with_increment_factory(int(instruction[20:]))
    elif instruction == 'deal into new stack':
        return reverse
    elif instruction.startswith('cut '):
        return cut_factory(int(instruction[4:]))
    else:
        raise NotImplementedError(instruction)


instructions = list(reversed([parse_instruction(i) for i in fileinput.input()]))
print()

card_position = initial_card_position
shuffle_count = 5000
seen_positions = {card_position}
for s in range(shuffle_count):
    for i in instructions:
        card_position = i(card_position)
    if card_position in seen_positions:
        print(f"Duplicate position spotted at {s} iterations")
        break
    seen_positions.add(card_position)
    # print(f"{s / shuffle_count * 100:.7f}")

print('Card in position 2020 is 2416342776788')
print(f"Card in position {initial_card_position} is {card_position}")
