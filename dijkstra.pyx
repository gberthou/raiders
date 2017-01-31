# All coordinates are in tile space
#cython: language_level=3
from libc.stdint cimport uint32_t, uint64_t, UINT64_MAX

# Used for any coordinates
ctypedef uint32_t coord_t
# Used for distances
ctypedef uint64_t dist_t
DIST_MAX = UINT64_MAX

cdef neighborsOf(pos):
    cdef coord_t x, y
    x, y = pos
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))

cdef dist_t calcDistance(p0, p1):
    cdef dist_t x0, x1, y0, y1
    x0, y0 = p0
    x1, y1 = p1
    return (x0 - x1)**2 + (y0 - y1)**2

# x1 > x0
# y1 > y0
cpdef dijkstra(area, start, goal):
    cdef coord_t x0, y0, x1, y1, startX, startY, goalX, goalY

    x0, y0, x1, y1 = area
    startX, startY = start
    goalX, goalY   = goal
    visitedSet     = set()
    prevMap        = dict()
    
    distMap = {(startX, startY) : 0}

    cdef dist_t distance, minDistance
    cdef long i 
    for i in range((x1-x0+1) * (y1-y0+1)):
        minDistance = DIST_MAX
        for point, distance in distMap.items():
            if distance < minDistance and (point not in visitedSet):
                minDistance = distance
                minDistPoint = point

        if minDistPoint[0] == goalX and minDistPoint[1] == goalY: # Mathematical proof of correctness?
            break

        visitedSet.add(minDistPoint)
        del distMap[minDistPoint]

        for neighbor in neighborsOf(minDistPoint):
            if neighbor in visitedSet:
                continue
            # What does "alt" stands for ?
            alt = minDistance + 1 + calcDistance(neighbor, goal) # A* like
            if neighbor not in distMap.keys() or alt < distMap[neighbor]:
                distMap[neighbor] = alt
                prevMap[neighbor] = minDistPoint
    return prevMap

def searchPath(area, start, goal):
    if start == goal:
        return [start]

    prevMap = dijkstra(area, start, goal)
    if goal not in prevMap.keys(): # No path
        return None

    path = [goal]
    lastPoint = goal
    while True:
        try:
            lastPoint = prevMap[lastPoint]
        except KeyError:
            break
        else:
            path.append(lastPoint)
    return reversed(path)

