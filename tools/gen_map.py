#!/usr/bin/python3

import sys
import random

random.seed()

opath = ""
width, height = 0, 0

if len(sys.argv) > 3:
    opath = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
else:
    print("Too few arguments: output file, width, height should be present")
    exit(1)


towrite = "{\n"

# Header
towrite += "\t\"width\": %d,\n\t\"height\": %d,\n" % (width, height)

# Tiles
"""
cols = []
for i in range(0, width):
    temp = "\t\"%d\":\n\t\t{\n" % i
    temp += ",\n".join(["\t\t\t\"%d\": %d" % (j, random.randint(1,5)) for j in range(0, height)])
    temp += "\n\t\t}"
    cols.append(temp)

towrite += ",\n".join(cols)
"""

tiles = [str(random.randint(1, 5)) for i in range(width * height)]
towrite += "\t\"tiles\": [%s],\n" % (",".join(tiles))

# Houses
# Format: [house, house, house]
# house = [housesetIndex, tileX, tileY]
towrite += "\t\"houses\": [[0, 5, 10]]"

towrite += "\n}"

with open(opath, "w+") as f:
    f.write(towrite)


