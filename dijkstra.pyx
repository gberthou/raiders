# All coordinates are in tile space
#cython: language_level=3
from libc.stdint cimport int32_t, int64_t, INT64_MAX
import collections

# Used for any coordinates
ctypedef int32_t coord_t
# Used for distances
ctypedef int64_t dist_t
DIST_MAX = INT64_MAX

cdef neighborsOf(pos):
    cdef coord_t x, y
    x, y = pos
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))

cdef dist_t calcDistance(p0, p1) except *:
    cdef dist_t x0, x1, y0, y1
    x0, y0 = p0
    x1, y1 = p1
    return (x0 - x1)**2 + (y0 - y1)**2

cdef edge(a, b):
    return min((a,b), (b,a))

# x1 > x0
# y1 > y0
cdef dijkstra(area, mapObstacles, start, goal):
    cdef coord_t x0, y0, x1, y1, startX, startY, goalX, goalY

    x0, y0, x1, y1 = area
    startX, startY = start
    goalX, goalY   = goal
    visitedSet     = set() | mapObstacles.nodes
    prevMap        = dict()
    
    distMap = {(startX, startY) : 0}

    walls = set(w.edge for w in mapObstacles.activeEdges())

    cdef dist_t distance, minDistance
    cdef long i 
    for i in range((x1-x0+1) * (y1-y0+1)):
        minDistance = DIST_MAX
        minDistPoint = None
        for point, distance in distMap.items():
            if distance < minDistance and (point not in visitedSet):
                minDistance = distance
                minDistPoint = point

        if minDistPoint == None:
            break

        if minDistPoint[0] == goalX and minDistPoint[1] == goalY: # Mathematical proof of correctness?
            break

        visitedSet.add(minDistPoint)
        del distMap[minDistPoint]

        for neighbor in neighborsOf(minDistPoint):
            if neighbor in visitedSet:
                continue
            # What does "alt" stand for? -> alternative distance I guess
            alt = minDistance + 1 + calcDistance(neighbor, goal) # A* like
            if neighbor not in distMap.keys() or alt < distMap[neighbor]:
                e = edge(neighbor, minDistPoint)
                if e not in walls:
                    distMap[neighbor] = alt
                    prevMap[neighbor] = minDistPoint
    return prevMap

def searchPath(area, mapObstacles, start, goal):
    if start == goal:
        return [start]
    
    prevMap = dijkstra(area, mapObstacles, start, goal)
    if goal not in prevMap.keys(): # No path
        return None

    path = collections.deque([goal])
    firstPoint = goal
    while True:
        try:
            firstPoint = prevMap[firstPoint]
        except KeyError:
            break
        else:
            path.appendleft(firstPoint)
    return path

