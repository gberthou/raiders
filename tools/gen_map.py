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

cols = []
for i in range(0, width):
    temp = "\t\"%d\":\n\t\t{\n" % i
    temp += ",\n".join(["\t\t\t\"%d\": %d" % (j, random.randint(1,5)) for j in range(0, height)])
    temp += "\n\t\t}"
    cols.append(temp)

towrite += ",\n".join(cols)
towrite += "\n}"

with open(opath, "w+") as f:
    f.write(towrite)


