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

DOMAIN_SPACE = 80
DOMAIN_PROBA = 0.3

FACTION_COUNT = 2

opath = ""
width, height = 0, 0

if len(sys.argv) > 3:
    opath = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
else:
    print("Too few arguments: output file, width, height should be present")
    exit(1)


# Generate map
mn = noise.MyNoise(1, 1, NOISE_NODE_COUNT)
t = [[mn.at(x/width, y/height) for x in range(width)] for y in range(height)] 
plt.imshow(t, interpolation="nearest")
plt.show()

tiles = [0] * (width * height)
for y in range(height):
    for x in range(width):
        index = x + y * width
        X = x / width
        Y = y / height

        z = mn.at(X, Y)
        if z < WATER_LEVEL:
            tiles[index] = 4
        else:
            dx, dy = mn.slopeAt(X, Y)
            slope = sqrt(dx*dx + dy*dy)
            if slope > MOUNTAIN_SLOPE:
                tiles[index] = 2
            else:
                tiles[index] = 0

#tiles = [str(random.randint(1, 5)) for i in range(width * height)]

domains = []
for y in range(height//DOMAIN_SPACE):
    for x in range(width//DOMAIN_SPACE):
        if random.random() < DOMAIN_PROBA:
            a = (x + random.random()) * DOMAIN_SPACE
            b = (y + random.random()) * DOMAIN_SPACE
            faction = random.randrange(FACTION_COUNT)
            domains.append([a, b, faction])

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


