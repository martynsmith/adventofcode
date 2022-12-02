from rich import print
import fileinput

def score_game_1(opp, me):
    # a = rock, b = paper, c = scissors
    # x = rock, y = paper, z = scissors
    match opp, me:
        case 'A', 'X': return 4
        case 'A', 'Y': return 8
        case 'A', 'Z': return 3
        case 'B', 'X': return 1
        case 'B', 'Y': return 5
        case 'B', 'Z': return 9
        case 'C', 'X': return 7
        case 'C', 'Y': return 2
        case 'C', 'Z': return 6
        case _:
            raise NotImplementedError(f"{opp=} {me=}")

def score_game_2(opp, me):
    # a = rock, b = paper, c = scissors
    # x = rock, y = paper, z = scissors
    match opp, me:
        case 'A', 'X': return 3
        case 'A', 'Y': return 4
        case 'A', 'Z': return 8
        case 'B', 'X': return 1
        case 'B', 'Y': return 5
        case 'B', 'Z': return 9
        case 'C', 'X': return 2
        case 'C', 'Y': return 6
        case 'C', 'Z': return 7
        case _:
            raise NotImplementedError(f"{opp=} {me=}")

part1 = 0
part2 = 0
for line in fileinput.input():
    part1 += score_game_1(line[0], line[2])
    part2 += score_game_2(line[0], line[2])

print("part1:", part1)
print("part2:", part2)
