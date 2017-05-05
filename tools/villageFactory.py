import random

SIZES = [(3, 3),
         (3, 5)]

REGULAR_HOUSE_ID = 0
INN_ID = 1

MIN_AMOUNT_HOUSES = 0
MAX_AMOUNT_HOUSES = 12

ORIENTATIONS = [lambda x,y : (x,y),
                lambda x,y : (y,-x),
                lambda x,y : (-x,-y),
                lambda x,y : (-y,x)]

def allPossibilities(area):
    x0, y0, x1, y1 = area
    t = [(x, y, o) for y in range(y0, int(y1)) for x in range(int(x0), int(x1)) for o in range(0, 4)]
    random.shuffle(t)
    return t

def isPossibilityValid(index, p, available, area):
    x0, y0, x1, y1 = area

    x, y, o = p
    w, h = SIZES[index]
    w, h = ORIENTATIONS[o](w, h)

    if x < x0 or x >= x1 or x+w < x0 or x+w >= x1 or y < y0 or y >= y1 or y+h < y0 or y+h >= y1:
        return False

    width = int(x1 - x0)
    for iy in range(y, y + h):
        for ix in range(x, x + w):
            if not available[ix-x0 + (iy-y0) * width]:
                return False
    return True

def updateAvailability(index, p, available, area):
    # Assumes that the possibility passed as parameter is valid
    x0, y0, x1, y1 = area

    x, y, o = p
    w, h = SIZES[index]
    w, h = ORIENTATIONS[o](w, h)
    width = int(x1 - x0)
    for iy in range(y, y + h):
        for ix in range(x, x + w):
            available[ix-x0 + (iy-y0) * width] = False

def genVillage(area):
    x0, y0, x1, y1 = area
    w = int(x1 - x0)
    h = int(y1 - y0)

    houses = []

    # Initial state: all slots are available
    available = [True] * (w * h)

    # First place the inn, since it is mandatory to every village
    innPossibilities = allPossibilities(area)
    # Take the first valid possibility - there is always one as long as the village is large enough for an inn
    while len(innPossibilities) and not isPossibilityValid(INN_ID, innPossibilities[0], available, area):
        del innPossibilities[0]

    if len(innPossibilities) == 0:
        raise Exception("Not enough room to place an inn")

    # Add valid inn position to the houses array
    houses.append([INN_ID] + list(innPossibilities[0]))
    # Remove inn slots from the available slots
    updateAvailability(INN_ID, innPossibilities[0], available, area)

    # Now place regular houses
    nRegularHouses = random.randint(MIN_AMOUNT_HOUSES, MAX_AMOUNT_HOUSES)

    # Try to place all regular houses
    for i in range(nRegularHouses):
        index = REGULAR_HOUSE_ID

        # All possibilities
        possibilities = allPossibilities(area)
        # Filter out invalid possibilities until the first valid one
        while len(possibilities) and not isPossibilityValid(index, possibilities[0], available, area):
            del possibilities[0]
        if len(possibilities): # If there is at least one valid possibility
            # Add valid position to the houses array
            houses.append([index] + list(possibilities[0]))
            # Remove slots from the available slots
            updateAvailability(index, innPossibilities[0], available, area)

    return houses

