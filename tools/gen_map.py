#!/usr/bin/python3

import sys
import random
from math import sqrt
from matplotlib import pyplot as plt

import noise

random.seed()

NOISE_NODE_COUNT = 40
WATER_LEVEL = 0.2
MIN_MOUNTAIN_SLOPE = 5
MAX_PLAIN_SLOPE = 1

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

def inWater(n, x, y):
    return n.at(x, y) < WATER_LEVEL
def inForest(n, x, y):
    z = n.at(x, y)
    dx, dy = n.slopeAt(x, y)
    slope = sqrt(dx*dx + dy*dy)
    return z >= WATER_LEVEL and slope >= MAX_PLAIN_SLOPE and slope < MIN_MOUNTAIN_SLOPE
def inMountain(n, x, y):
    dx, dy = n.slopeAt(x, y)
    slope = sqrt(dx*dx + dy*dy)
    return not inWater(n, x, y) and not inForest(n, x, y) and slope > MIN_MOUNTAIN_SLOPE

def generateTiles(n, width, height):
    tiles = [0] * (width * height)
    for y in range(height):
        for x in range(width):
            index = x + y * width
            X = x / width
            Y = y / height

            if inWater(n, X, Y):
                tiles[index] = 4
            elif inForest(n, X, Y):
                tiles[index] = 2
            elif inMountain(n, X, Y):
                tiles[index] = 3
            else:
                tiles[index] = 1
    return tiles

def generateDomains(n, width, height):
    MIN_SQUARE_DISTANCE = 25**2
    domains = []
    coordinates = [(x, y) for y in range(DOMAIN_SPACE) for x in range(DOMAIN_SPACE)]
    # Shuffle coordinates so that final distribution tends to be uniform
    random.shuffle(coordinates)
    for x, y in coordinates:
        extremum = n.localExtremum(x / DOMAIN_SPACE, y / DOMAIN_SPACE)
        if inWater(n, extremum[0], extremum[1]):
            continue
        extremum = (width * extremum[0], height * extremum[1])
        # Keep extremum only if not too close from the registered ones
        if sum([noise.d2(extremum, (i[0], i[1])) < MIN_SQUARE_DISTANCE for i in domains]) == 0:
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

def routesFromGraph(tiles, n, domains, graph, width, height):
    # No domain can be located inside a water tile (cf. generateDomains)
    for e in graph:
        p    = (int(domains[e[0]][0]), int(domains[e[0]][1]))
        goal = (int(domains[e[1]][0]), int(domains[e[1]][1]))
        path = {p}
        while p != goal:
            index = p[0] + p[1] * width
            # Set current tile as road
            tiles[index] = 5

            dx = sgn(goal[0] - p[0])
            dy = sgn(goal[1] - p[1])

            # Do not cross water (bridges yet to come?)
            if inWater(n, (p[0] + dx) / width, (p[1] + dy) / height):
                # t = array of (distance to goal, dx, dy)
                t = []
                for ax, ay in [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]:
                    q = (p[0] + ax, p[1] + ay)
                    if q in path or inWater(n, q[0] / width, q[1] / height):
                        continue
                    t.append((noise.d2(q, goal), ax, ay))
                # Sort array by distance to goal
                t.sort()
                # Take the closest solution to goal
                dx, dy = t[0][1:] # TODO: Sometimes crashes because t = [] when algorithm comes to a dead end

            if dx != 0 and dy != 0:
                # Set filler road tile so that there is no pure diagonal
                # (Manhattan distance between two adjacent road tiles should
                # always be 1)
                index = p[0] + dx + p[1] * width
                tiles[index] = 5

            p = (p[0] + dx , p[1] + dy)
            path = path.union({p})

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
routesFromGraph(tiles, mn, domains, graph, width, height)

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


