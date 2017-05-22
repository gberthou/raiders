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
cdef dijkstra(area, mapObstacles, start, goal, velocity = lambda x,y:1):
    cdef coord_t x0, y0, x1, y1
    x0, y0, x1, y1 = area
    visitedSet     = set() | mapObstacles.nodes
    prevMap        = dict()
    
    distMap = {start : (calcDistance(start, goal),0)} # Value format: (fScore, gScore)

    walls = set(w.edge for w in mapObstacles.activeEdges())

    cdef dist_t minF, f, gOfMinF, minDistance
    cdef long i 
    for i in range((x1-x0+1) * (y1-y0+1)):
        minF = DIST_MAX
        gOfMinF = DIST_MAX
        minFPoint = None
        for point, distances in distMap.items():
            f, g = distances
            if f < minF and (point not in visitedSet):
                minF = f
                gOfMinF = g
                minFPoint = point

        if minFPoint == None:
            break

        if minFPoint == goal: # Mathematical proof of correctness?
            break

        visitedSet.add(minFPoint)
        del distMap[minFPoint]

        for neighbor in neighborsOf(minFPoint):
            if neighbor in visitedSet:
                continue

            # If wall, ignore neighbor
            e = edge(neighbor, minFPoint)
            if e in walls:
                continue

            # TODO: change that into mapobstacles.nodes
            if velocity(neighbor[0], neighbor[1]) == 0:
                continue
            tentativeG = gOfMinF + 1 / velocity(neighbor[0], neighbor[1])
            if neighbor not in distMap.keys() or tentativeG < distMap[neighbor][1]:
                distMap[neighbor] = (tentativeG + calcDistance(neighbor, goal)/velocity(neighbor[0], neighbor[1]), tentativeG)
                prevMap[neighbor] = minFPoint
    return prevMap

def searchPath(area, mapObstacles, start, goal, velocity):
    if start == goal:
        return [start]
    
    prevMap = dijkstra(area, mapObstacles, start, goal, velocity)
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

