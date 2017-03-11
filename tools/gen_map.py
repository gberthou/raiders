#!/usr/bin/python3

import sys
import random

random.seed()

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
tiles = [str(random.randint(1, 5)) for i in range(width * height)]

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
towrite += "\t\"tiles\": [%s],\n" % (",".join(tiles))

# Houses
# Format: [house, house, house]
# house = [housesetIndex, tileX, tileY]
towrite += "\t\"houses\": [[0, 5, 10], [1, 10, 5]],\n"

# Domains
towrite += '\t"domains": [%s]' % (",".join(str(i) for i in domains))

towrite += "\n}"

with open(opath, "w+") as f:
    f.write(towrite)


