from rich import print
import fileinput

current = 0
part1 = 0
part2 = []

for line in fileinput.input():
    if not line.strip():
        part1 = max(current, part1)
        part2.append(current)
        current = 0
        continue
    current += int(line.strip())

part1 = max(current, part1)
part2.append(current)

print("part1:", part1)
print("part2:", sum(sorted(part2)[-3:]))

