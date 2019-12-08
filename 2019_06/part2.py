import fileinput
from collections import defaultdict
import networkx

graph = networkx.Graph()

data = [
    'COM)B',
    'B)C',
    'C)D',
    'D)E',
    'E)F',
    'B)G',
    'G)H',
    'D)I',
    'E)J',
    'J)K',
    'K)L',
    'K)YOU',
    'I)SAN',
]

for line in fileinput.input():
    hub, sat = line.strip().split(')')
    graph.add_edge(sat, hub)

print(networkx.dijkstra_path_length(graph, 'YOU', 'SAN') - 2)

