width = 25
height = 6

line = open('input.txt').read().strip()

layers = [line[i:i+width*height] for i in range(0, len(line), width*height)]

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
