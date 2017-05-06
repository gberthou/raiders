import random

# Always add 1 to the side that contains an external door, so that there will not be any door stuck in another house wall
SIZES = [(3, 4),
         (4, 5)]

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
    t = [(x, y, o) for y in range(y0, y1) for x in range(x0, x1) for o in range(0, 4)]
    random.shuffle(t)
    return t

def rangeAnyOrder(x, w):
    # Orientation can cause w (resp. h) to be negative, thus swapping (x) and (x+w) [resp. (y) and (y+h)] is required in such cases
    if w < 0:
        return range(x + w + 1, x + 1)
    return range(x, x + w)

def isPossibilityValid(index, p, available, area):
    x0, y0, x1, y1 = area

    x, y, o = p
    w, h = SIZES[index]
    w, h = ORIENTATIONS[o](w, h)

    if x < x0 or x >= x1 or x+w < x0 or x+w >= x1 or y < y0 or y >= y1 or y+h < y0 or y+h >= y1:
        return False

    width = x1 - x0

    for iy in rangeAnyOrder(y, h):
        for ix in rangeAnyOrder(x, w):
            if not available[ix-x0 + (iy-y0) * width]:
                return False
    return True

def updateAvailability(index, p, available, area):
    # Assumes that the possibility passed as parameter is valid
    x0, y0, x1, y1 = area

    x, y, o = p
    w, h = SIZES[index]
    w, h = ORIENTATIONS[o](w, h)

    width = x1 - x0
    for iy in rangeAnyOrder(y, h):
        for ix in rangeAnyOrder(x, w):
            available[ix-x0 + (iy-y0) * width] = False

def debugAvailable(available, area):
    x0, y0, x1, y1 = area
    width = x1 - x0
    height = y1 - y0
    for y in range(height):
        print("".join("1" if i else "0" for i in available[y*width:(y+1)*width]))

def genVillage(area):
    x0, y0, x1, y1 = area
    w = x1 - x0
    h = y1 - y0

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
            updateAvailability(index, possibilities[0], available, area)

    return houses

