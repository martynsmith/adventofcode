width = 25
height = 6

line = open('input.txt').read().strip()

layers = []

while len(line):
    layers.append(line[:width * height])
    line = line[width * height:]

current = "2" * width * height

for layer in layers:
    for pos, pixel in enumerate(layer):
        if current[pos] == "2":
            current = current[:pos] + pixel + current[pos + 1:]

print('---')
current = current.replace('0', " ")
current = current.replace('1', u"\u2588")
current = current.replace('2', "?")
while len(current):
    print(current[:width])
    current = current[width:]
