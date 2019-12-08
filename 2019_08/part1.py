width = 25
height = 6

line = open('input.txt').read().strip()

layers = []

while len(line):
    layers.append(line[:width * height])
    line = line[width * height:]

zero_count = width * height
one_two = None

for layer in layers:
    if layer.count("0") < zero_count:
        zero_count = layer.count("0")
        one_two = layer.count("1") * layer.count("2")

print(one_two)

