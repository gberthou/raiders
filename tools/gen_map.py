#!/usr/bin/python3

import sys
import random
from math import sqrt
from matplotlib import pyplot as plt

import noise

random.seed()

NOISE_NODE_COUNT = 40
WATER_LEVEL = 0.2
MOUNTAIN_SLOPE = 0.1

DOMAIN_SPACE = 10
DOMAIN_PROBA = 0.3

FACTION_COUNT = 2

opath = ""
width, height = 0, 0

def edge(a, b):
    return (min(a, b), max(a, b))
def sgn(x):
    if x == 0:
        return 0
    if x < 0:
        return -1
    return 1

def generateTiles(n, width, height):
    tiles = [0] * (width * height)
    for y in range(height):
        for x in range(width):
            index = x + y * width
            X = x / width
            Y = y / height

            z = n.at(X, Y)
            if z < WATER_LEVEL:
                tiles[index] = 4
            else:
                dx, dy = n.slopeAt(X, Y)
                slope = sqrt(dx*dx + dy*dy)
                if slope > MOUNTAIN_SLOPE:
                    tiles[index] = 2
                else:
                    tiles[index] = 0
    return tiles

def generateDomains(n, width, height):
    domains = []
    for y in range(DOMAIN_SPACE):
        for x in range(DOMAIN_SPACE):
            extremum = n.localExtremum(x / DOMAIN_SPACE, y / DOMAIN_SPACE)
            extremum = (width * extremum[0], height * extremum[1])
            # Keep extremum only if not registered yet
            if sum([noise.d2(extremum, (i[0], i[1]))<1 for i in domains]) == 0:
                faction = random.randrange(FACTION_COUNT)
                domains.append([extremum[0], extremum[1], faction])

    # Remove random domains if they are too numerous
    while len(domains) > 64:
        del domains[random.randint(0, len(domains))]

    return domains

def domainGraph(domains):
    graph = set()
    coveredDomains = set()
    domainCount = len(domains)

    # Compute pairwise distances
    distances = []
    for i in range(domainCount):
        t = [noise.d2((domains[i][0], domains[i][1]), (domains[j][0], domains[j][1])) for j in range(i)]
        distances.append(t)

    # For all Origin in Domains
    for i in range(domainCount):
        # Get distance between Origin and all other nodes
        t = [(distances[max(i, j)][min(i, j)], j) for j in range(domainCount) if i != j]
        t.sort()
        # Add the 3 closest domains as edges, if not already present
        graph = graph.union({edge(i, item[1]) for item in t[:3]})

    return graph

def routesFromGraph(tiles, domains, graph, width):
    for e in graph:
        p    = (int(domains[e[0]][0]), int(domains[e[0]][1]))
        goal = (int(domains[e[1]][0]), int(domains[e[1]][1]))
        while p != goal:
            index = p[0] + p[1] * width
            # Set current tile as road
            tiles[index] = 5

            dx = goal[0] - p[0]
            dy = goal[1] - p[1]
            p = (p[0] + sgn(dx) , p[1] + sgn(dy))

def setDomainsAsDebug(tiles, domains, width):
    for d in domains:
        index = int(d[0]) + int(d[1]) * width
        tiles[index] = 6
        
"""
for y in range(height//DOMAIN_SPACE):
    for x in range(width//DOMAIN_SPACE):
        if random.random() < DOMAIN_PROBA:
            a = (x + random.random()) * DOMAIN_SPACE
            b = (y + random.random()) * DOMAIN_SPACE
            faction = random.randrange(FACTION_COUNT)
            domains.append([a, b, faction])
"""

if len(sys.argv) > 3:
    opath = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
else:
    print("Too few arguments: output file, width, height should be present")
    exit(1)


# Create noise
mn = noise.MyNoise(1, 1, NOISE_NODE_COUNT)

# Debug display
t = [[mn.at(x/100, y/100) for x in range(101)] for y in range(101)] 
plt.imshow(t, interpolation="nearest")
plt.show()

# Generate map
print("Generating tiles...")
tiles = generateTiles(mn, width, height)

domains = []
# Create domains. Domain center is a local extremum
print("Generating domains...")
domains = generateDomains(mn, width, height)

# Generate roads
print("Generating roads...")
graph = domainGraph(domains)
routesFromGraph(tiles, domains, graph, width)

# Debug
setDomainsAsDebug(tiles, domains, width)

# Output
towrite = "{\n"

# Header
towrite += "\t\"width\": %d,\n\t\"height\": %d,\n" % (width, height)

# Tiles
towrite += "\t\"tiles\": [%s],\n" % (",".join(str(i) for i in tiles))

# Houses
# Format: [house, house, house]
# house = [housesetIndex, tileX, tileY]
towrite += "\t\"houses\": [[0, 5, 10], [1, 10, 5]],\n"

# Domains
towrite += '\t"domains": [%s]' % (",".join(str(i) for i in domains))

towrite += "\n}"

with open(opath, "w+") as f:
    f.write(towrite)


