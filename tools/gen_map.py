#!/usr/bin/python3

import sys
import random
from math import sqrt, floor
from matplotlib import pyplot as plt

import noise
import villageFactory
import dijkstra

random.seed()

NOISE_NODE_COUNT = 16
WATER_LEVEL = 0.2
MIN_MOUNTAIN_SLOPE = 5
MAX_PLAIN_SLOPE = 1

MAX_VILLAGE_SIZE = 24

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
    MIN_SQUARE_DISTANCE = (MAX_VILLAGE_SIZE*2)**2
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

def genVillages(domains, width, height):
    houses = []
    for x, y, _ in domains:
        x0 = floor(max(0, x - MAX_VILLAGE_SIZE/2))
        x1 = floor(min(width, x + MAX_VILLAGE_SIZE/2))
        y0 = floor(max(0, y - MAX_VILLAGE_SIZE/2))
        y1 = floor(min(height, y + MAX_VILLAGE_SIZE/2))
        houses.extend(villageFactory.genVillage((x0, y0, x1, y1)))
    return houses

# nodes: [(x0, y0), (x1, y1), ...]
def routeGraph(nodes):
    graph = set()
    coveredNodes = set()
    nodeCount = len(nodes)

    # Compute pairwise distances
    distances = []
    for i in range(nodeCount):
        t = [noise.d2((nodes[i][0], nodes[i][1]), (nodes[j][0], nodes[j][1])) for j in range(i)]
        distances.append(t)

    # For all Origin in Domains
    for i in range(nodeCount):
        # Get distance between Origin and all other nodes
        t = [(distances[max(i, j)][min(i, j)], j) for j in range(nodeCount) if i != j]
        t.sort()
        # Add the 3 closest domains as edges, if not already present
        graph = graph | {edge(i, item[1]) for item in t[:3]}

    return graph

def routesFromGraph(tiles, nodes, graph, width, height):
    # Assumes that no node is inside a water tile or an indoor tile

    # forbiddenTiles: All tiles that are water or indoors
    class DijkstraObstacles:
        def __init__(self, forbiddenTiles):
            self.nodes = forbiddenTiles

        def activeEdges(self):
            return set()

    # TODO: Magical values
    forbiddenTiles = set((x, y) for y in range(height) for x in range(width) if tiles[x + y*width] == 4 or tiles[x + y*width] == 7)
    mapObstacles = DijkstraObstacles(forbiddenTiles)

    for e in graph:
        p    = (int(nodes[e[0]][0]), int(nodes[e[0]][1]))
        goal = (int(nodes[e[1]][0]), int(nodes[e[1]][1]))
        
        path = dijkstra.searchPath((0, 0, width, height), mapObstacles, p, goal)
        for position in path:
            x, y = position
            # TODO: Magical values
            tiles[x + y * width] = 5

def setDomainsAsDebug(tiles, domains, width):
    for d in domains:
        index = int(d[0]) + int(d[1]) * width
        tiles[index] = 6

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

# Create villages
print("Generating villages...")
houses = genVillages(domains, width, height)
villageFactory.houses2tiles(houses, tiles, width)

# Generate roads
print("Generating roads...")
inns          = [h.absoluteDoorPosition() for h in houses if h.isInn()]
regularHouses = [h.absoluteDoorPosition() for h in houses if not h.isInn()]
innGraph = routeGraph(inns)
housesGraph = routeGraph(regularHouses)
routesFromGraph(tiles, inns, innGraph, width, height)
routesFromGraph(tiles, regularHouses, housesGraph, width, height)

# Output
towrite = "{\n"

# Header
towrite += "\t\"width\": %d,\n\t\"height\": %d,\n" % (width, height)

# Tiles
towrite += "\t\"tiles\": [%s],\n" % (",".join(str(i) for i in tiles))

# Houses
# Format: [house, house, house]
# house = [housesetIndex, tileX, tileY, orientation]
towrite += "\t\"houses\": [%s],\n" % (",".join(str(h) for h in houses))

# Domains
towrite += '\t"domains": [%s]' % (",".join(str(i) for i in domains))

towrite += "\n}"

with open(opath, "w+") as f:
    f.write(towrite)


