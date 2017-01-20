#!/usr/bin/python3

import sys, re


if len(sys.argv) < 0:
    print("fuck")
    exit(1)

input_fname = sys.argv[1]

input_file = []
output = "# Generated file: do not edit, use gen_comps.py instead\n\nimport ecs\n\n"

with open(input_fname, "r") as f:
    input_file = f.readlines()

for line in input_file:
    comps = re.sub(r"[ \n]", "", line).split(",")
    if len(comps) < 2:
        continue

    output += "def %s(Component):\n" % comps[0]
    output += "%sdef __init__(%s):\n" % (" "*4, ",".join(comps[1:]))

    for comp in comps[1:]:
        output += "%sself.%s = %s\n" % (" "*8, comp, comp)

    output += "\n"

with open("components.py","w") as f:
    f.write(output)






